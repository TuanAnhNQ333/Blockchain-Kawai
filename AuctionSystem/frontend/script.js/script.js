document.addEventListener("DOMContentLoaded", async function() {
    const auctionItems = document.getElementById("auction-items");
    const featuredItems = document.getElementById("featured-items");

    try {
        // Fetch auction items from backend API
        const response = await fetch('http://localhost:8000/auctions');
        const items = await response.json();

        // Render auction items
        items.forEach(item => {
            const auctionCard = createAuctionCard(item);
            auctionItems.appendChild(auctionCard);
        });

        // Show featured items (top 3 by price)
        const featuredAuctions = items
            .sort((a, b) => b.starting_price - a.starting_price)
            .slice(0, 3);
            
        featuredAuctions.forEach(item => {
            const featuredCard = createAuctionCard(item, true);
            featuredItems.appendChild(featuredCard);
        });

    } catch (error) {
        console.error('Error fetching auction data:', error);
        showErrorMessage('Không thể tải dữ liệu đấu giá');
    }
});

function createAuctionCard(item, isFeatured = false) {
    const card = document.createElement('div');
    card.className = `auction-card ${isFeatured ? 'featured' : ''}`;
    
    card.innerHTML = `
        <div class="auction-image">
            <img src="${item.image || 'placeholder.jpg'}" alt="${item.name}">
        </div>
        <div class="auction-details">
            <h3>${item.name}</h3>
            <p>${item.description}</p>
            <div class="price-info">
                <span class="starting-price">Giá khởi điểm: ${formatCurrency(item.starting_price)}</span>
                <span class="current-bid">Giá hiện tại: ${formatCurrency(item.current_bid || item.starting_price)}</span>
            </div>
            <button class="bid-button" onclick="placeBid(${item.id})">Đặt giá</button>
        </div>
    `;
    
    return card;
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
}

function showErrorMessage(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    setTimeout(() => errorDiv.remove(), 5000);
}

async function placeBid(auctionId) {
    // Implement bid placement logic here
    const bidAmount = prompt('Nhập số tiền muốn đặt:');
    if (!bidAmount) return;

    try {
        const response = await fetch('http://localhost:8000/bids', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                auction_id: auctionId,
                bidder_name: 'User', // Should come from authentication
                bid_amount: parseFloat(bidAmount)
            })
        });

        if (response.ok) {
            alert('Đặt giá thành công!');
            location.reload(); // Refresh to show updated prices
        } else {
            const error = await response.json();
            alert(`Lỗi: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error placing bid:', error);
        alert('Có lỗi xảy ra khi đặt giá');
    }
}