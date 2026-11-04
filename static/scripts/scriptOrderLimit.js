async function LoadOrder(limit = null) {
    const container = document.querySelector
    ('#orders-container');
    container.innerHTML = "<p style='color: black
    ;'>Loading...</p>";

    try {
        const url = limit ? `/order/limit
        /${limit}` : '/orders';
        const response = await fetch(url);
        if (!response.ok) throw new Error('Server error');

        const orders = await response.json();

        container.innerHTML = '';
        if (orders.length === 0) {
            container.innerHTML = "<h1 style='color: white; text-align: center;'>There are no application yet.</h1>";
            return;
        }
        orders.forEach(order => {
            const a = document.createElement('a');
            a.href = `/ui/order/${order.id}`;
            a.className = 'card-order';
            const h1 = document.createElement('h1');
            h1.className = 'card-order-name';
            h1.textContent = `Order from: @${order.username} | Status: ${order.status} | Time: ${order.created_at}`;
            const p = document.createElement('p');
            p.className = 'card-order-title';
            p.textContent = order.description;
            
            a.appendChild(h1);
            a.appendChild(p);
            container.appendChild(a);
        });

    } catch(error) {
        container.textContent = `Error: ${error.message}`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    LoadOrder();
    
    const btn5 = document.querySelector('#limit-5');
    if (btn5) btn5.onclick = () => LoadOrder(5);
    const btn10 = document.querySelector('#limit-10');
    if (btn10) btn10.onclick = () => LoadOrder(10);
    const btn20 = document.querySelector('#limit-20');
    if (btn20) btn20.onclick = () => LoadOrder(20);
    const btn45 = document.querySelector('#limit-45');
    if (btn45) btn45.onclick = () => LoadOrder(45);
});