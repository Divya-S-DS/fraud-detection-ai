const form = document.getElementById('fraudForm');

form.addEventListener('submit', async function(e) {

    e.preventDefault();

    const formData = new FormData(form);

    const response = await fetch('/predict', {

        method: 'POST',

        body: formData
    });

    const data = await response.json();

    let html = '';

    html += `
        <h2>
            Fraud Probability:
            ${data.probability}%
        </h2>
    `;

    if(data.fraud) {

        html += `
            <h3 style="color:red;">
                High Risk Transaction
            </h3>
        `;

    } else {

        html += `
            <h3>
                Safe Transaction
            </h3>
        `;
    html += `<h4>Reasons:</h4>`;

    html += '<ul>';

    data.reasons.forEach(reason => {

        html += `<li>${reason}</li>`;
    });

    html += '</ul>';
    document.getElementById('result').innerHTML = html;
    }
});