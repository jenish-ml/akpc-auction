from django.db.models import Max, Count, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Player, UserProfile, Bid
from .forms import CustomUserCreationForm, PlayerForm, BidForm

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
    players = Player.objects.all()
    
    # Handle search query
    search_query = request.GET.get('search', '')
    if search_query:
        players = players.filter(
            Q(name__icontains=search_query) |
            Q(position__icontains=search_query) |
            Q(playing_style__icontains=search_query)
        )
    
    # Handle position filter
    position_filter = request.GET.get('position', '')
    if position_filter:
        players = players.filter(position=position_filter)
    
    return render(request, 'player_list.html', {
        'players': players,
        'search_query': search_query,
        'position_filter': position_filter,
        'position_choices': Player.POSITION_CHOICES
    })

@login_required
def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    bids = Bid.objects.filter(player=player).order_by('-amount')
    
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.player = player
            bid.user = request.user
            bid.save()
            messages.success(request, 'Your bid has been placed!')
            return redirect('player_detail', pk=pk)
    else:
        form = BidForm()
    
    return render(request, 'player_detail.html', {
        'player': player,
        'bids': bids,
        'form': form
    })

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_bid_view(request):
    # Your view logic here
    bids = Bid.objects.all().order_by('-timestamp')
    return render(request, 'admin/bid_view.html', {'bids': bids})

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
@login_required
def admin_bid_view(request):
    # Get all players with their highest bids
    players_with_bids = Player.objects.annotate(
        highest_bid=Max('bid__amount'),
        bid_count=Count('bid')
    ).order_by('-highest_bid')
    
    # Calculate statistics in the view
    total_players = players_with_bids.count()
    players_with_bids_count = players_with_bids.filter(bid_count__gt=0).count()
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

