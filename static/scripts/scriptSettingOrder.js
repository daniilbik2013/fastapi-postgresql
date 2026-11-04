const pathParts = window.location.pathname.split('/');
const orderId = pathParts[pathParts.length - 1];

async function LoadOrder() {
    try {
        const response = await fetch(`/orders/${orderId}`);
        
        if (!response.ok) throw new Error('Заказ не найден');
        const order = await response.json();
        
        document.querySelector('.card-order').innerHTML = `
            <h1 class='card-order-name'>Order from: @${order.username}<br>Phone: ${order.number}</h1>
            <p class='card-order-title'>
                Title:<br><span class='smalltext'>${order.title}</span><br><br>
                Description:<br><span class='smalltext'>${order.description}</span>
            </p>
        `;
        
        document.querySelector('#deleteBtn').onclick = () => deleteOrder(orderId);
        document.querySelector('#statusBtn_progress').onclick = () => setStatus(orderId, 'in_progress');
        document.querySelector('#statusBtn_done').onclick = () => setStatus(orderId, 'done');
    } catch(error) {
        document.querySelector('.card-order').innerHTML = `<h1 style="color:red;">Ошибка: ${error.message}</h1>`;
    }
}

async function deleteOrder(id) {
	if (!confirm("Are you sure to delete this request?")) return;
	
	const response = await fetch(`/delete_order/${id}`, {
		method: 'DELETE'
	});
	const result = await response.json();
	
	if (result.success) {
		window.location.href = '/';
	} else {
		alert('Произошла ошибка ' + (result.detail || 'Пожалуйста, отправте содержимое в Телеграм @duovss'))
	}
}
async function setStatus(id, new_status) {
	if (!confirm('Are you sure you want to change the application status?')) return;
	const response = await fetch(`/update_order/${id}`, {
		method: 'PATCH',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify({ status: new_status})
		});
		const result = await response.json();
		if (result.success) {
			location.reload();
		} else {
			alert('Ошибка: ' + result.detail)
		}
}

document.addEventListener('DOMContentLoaded', LoadOrder);