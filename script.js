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