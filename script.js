async function calculate() {
    const num1 = parseFloat(document.getElementById('num1').value);
    const num2 = parseFloat(document.getElementById('num2').value);
    const operator = document.getElementById('operator').value;

    const response = await fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ num1, num2, operator })
    });

    const data = await response.json();
    if (response.ok) {
        document.getElementById('result').innerText = '结果: ' + data.result;
    } else {
        document.getElementById('result').innerText = '错误: ' + data.error;
    }
}

let currentId = null;

async function getHistory(action) {
    let id;
    if (action === 'first') {
        id = 1;
    } else if (action === 'last') {
        const response = await fetch('/history');
        const data = await response.json();
        id = data[data.length - 1].id;
    } else if (action === 'prev' && currentId > 1) {
        id = currentId - 1;
    } else if (action === 'next') {
        const response = await fetch('/history');
        const data = await response.json();
        id = currentId + 1;
        if (id > data[data.length - 1].id) {
            id = data[data.length - 1].id;
        }
    } else if (action === 'current' && currentId) {
        id = currentId;
    } else {
        return;
    }

    const response = await fetch(`/history/${id}`);
    const data = await response.json();
    if (response.ok) {
        document.getElementById('num1').value = data.Data1;
        document.getElementById('operator').value = data.CalcType;
        document.getElementById('num2').value = data.Data2;
        document.getElementById('result').innerText = '结果: ' + data.Result;
        currentId = data.id;
    } else {
        document.getElementById('result').innerText = '错误: ' + data.error;
    }
}