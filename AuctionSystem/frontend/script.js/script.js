document.addEventListener("DOMContentLoaded", function() {
    const auctionItems = document.getElementById("auction-items");

    // fetch auction items from the backend (fake data for now)
    const items = [
        { id: 1, name: "Laptop gaming", price: 500},
        { id: 2, name: "Smartphone", price: 300},
        { id: 3, name: "Camera DSLR", price: 450}
    ];

    items.forEach(item => {
        const li = document.createElement("li");
        li.innerHTML = '<strong>${item.name}</strong> - Starting bid: $${item.price';
        auctionItems.appendChild(li);
    });
});