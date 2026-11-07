const contact = document.querySelector('#contact');const modal = document.querySelector('#modal');

if (contact && modal) {
	contact.addEventListener('click', () => {
		modal.classList.toggle('active');
});
}

async function LoadOrder() {
	const container = document.querySelector('.cards-order');
	container.innerHTML = "<p style='color: black;'>Loading...</p>";
	try {
		const response = await fetch('/api/last-orders');
		if (!response.ok) throw new Error('Server Error');
		
		const orders = await response.json();
		
		container.innerHTML = "";
		
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
			h1.textContent = ``Order from: @${order.username} | Status: ${order.status} | Time: ${order.created_at}`;
			const p = document.createElement('p');
			p.className = 'card-order-title';
			p.style.paddingLeft = '10px';
			p.textContent = order.title;
			
			a.appendChild(h1);
			a.appendChild(p);
            container.appendChild(a);
		});
	} catch(error) {
		container.innerHTML = `<h1 style='color: #D00000; font-size: 23px;'>Error: ${error.message}</h1>`;
	}
}

document.addEventListener('DOMContentLoaded', () => {

LoadOrder();

});