from django.db.models import Max, Count, Sum, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Player, UserProfile, Bid, Team, Transaction
from .forms import CustomUserCreationForm, PlayerForm, BidForm, UsernameChangeForm

def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'Registration successful! Please wait for admin approval.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                profile = user.userprofile
                if profile.is_approved:
                    login(request, user)
                    return redirect('player_list')
                else:
                    messages.error(request, 'Your account is pending admin approval.')
            except UserProfile.DoesNotExist:
                messages.error(request, 'Invalid account.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def player_list(request):
    players = Player.objects.filter(team__isnull=True)
    
    search_query = request.GET.get('search', '')
    if search_query:
        players = players.filter(
            Q(name__icontains=search_query) |
            Q(position__icontains=search_query) |
            Q(playing_style__icontains=search_query)
        )

    
    position_filter = request.GET.get('position', '')
    if position_filter:
        players = players.filter(position=position_filter)
        
    rating_filter = request.GET.get('rating', '')
    if rating_filter:
        players = players.filter(rating=rating_filter)
        
    paginator = Paginator(players, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'player_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'position_filter': position_filter,
        'rating_filter': rating_filter,
        'position_choices': Player.POSITION_CHOICES,
        'rating_choices': ['5⭐️', '4⭐️', '3⭐️'],
    })

@login_required
def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    bids = Bid.objects.filter(player=player).order_by('-amount')
    
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['amount']
            try:
                team = getattr(request.user, 'userprofile', None) and request.user.userprofile.team
                if not team:
                    messages.error(request, 'You are not assigned to a team.')
                    return redirect('player_detail', pk=pk)
                
                if player.team:
                    messages.error(request, f'This player has already been purchased by {player.team.name}.')
                    return redirect('player_detail', pk=pk)

                if team.players.count() >= 13:
                    messages.error(request, 'Your squad already has the maximum of 13 players.')
                    return redirect('player_detail', pk=pk)
                
                if player.rating == '5⭐️' and team.players.filter(rating='5⭐️').count() >= 7:
                    messages.error(request, 'Your squad already has the maximum of 7 5⭐️ players.')
                    return redirect('player_detail', pk=pk)

                # Fetch highest existing pending bid to validate new bid amount
                highest_existing_bid = Bid.objects.filter(player=player, status='PENDING').aggregate(Max('amount'))['amount__max']
                if highest_existing_bid and bid_amount <= highest_existing_bid:
                    messages.error(request, f'Your bid of ${bid_amount}M is too low! You must bid higher than the current pending bid of ${highest_existing_bid}M.')
                    return redirect('player_detail', pk=pk)

                pending_bids_total = Bid.objects.filter(user__userprofile__team=team, status='PENDING').aggregate(Sum('amount'))['amount__sum'] or 0
                available_balance = team.balance - pending_bids_total

                if available_balance < bid_amount:
                    messages.error(request, f'Insufficient available balance! You have ${team.balance}M total, but ${pending_bids_total}M is locked in pending bids. Available: ${available_balance}M.')
                else:
                        bid = form.save(commit=False)
                        bid.player = player
                        bid.user = request.user
                        bid.status = 'PENDING'
                        bid.save()
                        
                        # Automatically unlock previous locked funds by rejecting all older pending bids
                        Bid.objects.filter(player=player, status='PENDING').exclude(id=bid.id).update(status='REJECTED')
                        
                        messages.success(request, f'Successfully placed highest bid of ${bid_amount}M for {player.name}! Previous bidders have had their funds restored.')
            except Exception as e:
                messages.error(request, 'An error occurred processing your bid.')
                
            return redirect('player_detail', pk=pk)
    else:
        form = BidForm()
    
    team = getattr(request.user, 'userprofile', None) and request.user.userprofile.team
    pending_bids_total = 0
    available_balance = 0
    if team:
        pending_bids_total = Bid.objects.filter(user__userprofile__team=team, status='PENDING').aggregate(Sum('amount'))['amount__sum'] or 0
        available_balance = team.balance - pending_bids_total
    
    return render(request, 'player_detail.html', {
        'player': player,
        'bids': bids,
        'form': form,
        'team': team,
        'pending_bids_total': pending_bids_total,
        'available_balance': available_balance
    })

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
@login_required
def admin_bid_view(request):
    players_with_bids = Player.objects.annotate(
        highest_bid=Max('bids__amount'),
        bid_count=Count('bids')
    ).filter(bid_count__gt=0).order_by('-highest_bid')
    
    total_players = players_with_bids.count()
    players_with_bids_count = players_with_bids.count()
    total_bids = Bid.objects.count()
    
    return render(request, 'admin_bid_view.html', {
        'players_with_bids': players_with_bids,
        'total_players': total_players,
        'players_with_bids_count': players_with_bids_count,
        'total_bids': total_bids,
    })

@user_passes_test(is_admin)
@login_required
def player_bid_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    bids = Bid.objects.filter(player=player).order_by('-amount')
    
    return render(request, 'admin_player_bids.html', {
        'player': player,
        'bids': bids
    })

@user_passes_test(is_admin)
@login_required
def admin_dashboard_view(request):
    teams = Team.objects.all().order_by('league', '-balance').prefetch_related('players')
    transactions = Transaction.objects.all().order_by('-created_at')[:100]
    
    total_balance = teams.aggregate(Sum('balance'))['balance__sum'] or 0
    total_bids = Bid.objects.count()
    
    return render(request, 'admin_dashboard.html', {
        'teams': teams,
        'transactions': transactions,
        'total_balance': total_balance,
        'total_bids': total_bids,
        'league_choices': Team.LEAGUE_CHOICES,
    })

@login_required
def team_profile(request, team_id=None):
    if team_id:
        team = get_object_or_404(Team, id=team_id)
    else:
        team = getattr(request.user, 'userprofile', None) and request.user.userprofile.team
        
    if not team:
        messages.error(request, 'You are not assigned to a team.')
        return redirect('player_list')
        
    players = team.players.all()
    five_star_count = players.filter(rating='5⭐️').count()
    
    # Extract Bidding History globally for this specific team's linked users
    my_bids = Bid.objects.filter(user__userprofile__team=team).select_related('player').order_by('-created_at')[:60]
    
    # Extract Mathematical Leaders. Because our 'place_bid' natively mass-rejects inferior bids, 
    # any bid remaining in PENDING status owned by this team is unequivocally the leading bid globally.
    highest_bids = Bid.objects.filter(user__userprofile__team=team, status='PENDING').select_related('player').order_by('-amount')
    
    return render(request, 'team_profile.html', {
        'team': team,
        'players': players,
        'five_star_count': five_star_count,
        'my_bids': my_bids,
        'highest_bids': highest_bids,
        'is_own_profile': team_id is None or getattr(request.user.userprofile, 'team', None) == team
    })

@login_required
def all_players_database(request):
    players = Player.objects.all().select_related('team')
    
    search_query = request.GET.get('search', '')
    if search_query:
        players = players.filter(
            Q(name__icontains=search_query) |
            Q(position__icontains=search_query) |
            Q(playing_style__icontains=search_query)
        )
    
    position_filter = request.GET.get('position', '')
    if position_filter:
        players = players.filter(position=position_filter)
        
    rating_filter = request.GET.get('rating', '')
    if rating_filter:
        players = players.filter(rating=rating_filter)
        
    paginator = Paginator(players, 48) # Many players per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'all_players.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'position_filter': position_filter,
        'rating_filter': rating_filter,
        'position_choices': Player.POSITION_CHOICES,
        'rating_choices': ['5⭐️', '4⭐️', '3⭐️'],
    })

@user_passes_test(is_admin)
@login_required
def delete_bid_action(request, bid_id):
    if request.method == 'POST':
        bid = get_object_or_404(Bid, id=bid_id)
        player = bid.player
        team = getattr(bid.user, 'userprofile', None) and bid.user.userprofile.team
        
        # Undo the purchase if team matches the current owner AND bid was Approved
        if team and player.team == team and bid.status == 'APPROVED':
            team.balance += bid.amount
            team.save()
            Transaction.objects.create(
                team=team,
                amount=bid.amount,
                description=f"Refund: Admin deleted approved bid for {player.name}"
            )
            player.team = None
            player.save()
            
        bid.delete()
        messages.success(request, f"Bid for {player.name} deleted successfully.")
        
    return redirect('player_bid_detail', player_id=player.id)

@user_passes_test(is_admin)
@login_required
def approve_bid_action(request, bid_id):
    if request.method == 'POST':
        bid = get_object_or_404(Bid, id=bid_id)
        player = bid.player
        team = getattr(bid.user, 'userprofile', None) and bid.user.userprofile.team
        
        if bid.status == 'APPROVED':
            messages.info(request, "This bid is already approved.")
            return redirect('player_bid_detail', player_id=player.id)
            
        if player.team:
            messages.error(request, f"{player.name} is already assigned to a team.")
            return redirect('player_bid_detail', player_id=player.id)
            
        if not team:
            messages.error(request, "The user who placed this bid is not assigned to a team.")
            return redirect('player_bid_detail', player_id=player.id)
            
        if team.balance < bid.amount:
            messages.error(request, f"Team {team.name} has insufficient balance to cover this bid.")
            return redirect('player_bid_detail', player_id=player.id)
            
        # Execute Purchase
        team.balance -= bid.amount
        team.save()
        
        Transaction.objects.create(team=team, amount=-bid.amount, description=f"Won bid for {player.name}")
        
        player.team = team
        player.save()
        
        bid.status = 'APPROVED'
        bid.save()
        
        # Reject all other pending bids for this player
        Bid.objects.filter(player=player, status='PENDING').exclude(id=bid.id).update(status='REJECTED')
        
        messages.success(request, f"Bid approved! {player.name} assigned to {team.name}.")
    
    return redirect('player_bid_detail', player_id=player.id)

@user_passes_test(is_admin)
@login_required
def reject_bid_action(request, bid_id):
    if request.method == 'POST':
        bid = get_object_or_404(Bid, id=bid_id)
        if bid.status == 'PENDING':
            bid.status = 'REJECTED'
            bid.save()
            messages.success(request, "Bid rejected.")
        else:
            messages.error(request, "Only pending bids can be rejected.")
    return redirect('player_bid_detail', player_id=bid.player.id)

@user_passes_test(is_admin)
@login_required
def admin_add_player(request):
    teams = Team.objects.all().order_by('name')
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        rating = request.POST.get('rating')
        market_value = float(request.POST.get('market_value') or 0)
        team_id = request.POST.get('team')
        
        player = Player(
            name=name,
            position=position,
            rating=rating,
            base_price=market_value
        )
        if hasattr(player, 'market_value'):
            player.market_value = market_value
            
        if team_id:
            team = Team.objects.get(id=team_id)
            player.team = team
        
        player.save()
        messages.success(request, f"Player {name} successfully added to the database.")
        return redirect('admin_dashboard')
        
    return render(request, 'admin_add_player.html', {
        'teams': teams,
        'position_choices': Player.POSITION_CHOICES,
        'rating_choices': ['5⭐️', '4⭐️', '3⭐️'],
    })

@login_required
def edit_username(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your username has been successfully updated!')
            return redirect('team_profile')
    else:
        form = UsernameChangeForm(instance=request.user)
    return render(request, 'edit_username.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('team_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})
