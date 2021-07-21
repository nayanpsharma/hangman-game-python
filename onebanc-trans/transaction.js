async function getTransactions() {
    const url = 'https://dev.onebanc.ai/assignment.asmx/GetTransactionHistory?userId=1&recipientId=2';
    const response = await fetch(url);
    var data = await response.json();
    const dateSet = getDateSet(data.transactions);

    let html = ``;

    for (i of dateSet) {
        html += `
        <h2> <span>${i}</span> </h2>`;
        for (a of data.transactions) {
            let temp = new Date(a.startDate);
            let displayDate = moment(temp).format('Do MMM YYYY, h:mm a');
            let localeString = temp.toLocaleDateString();
            if (i === localeString) {

                if (a.type == 1 && a.direction == 1) {
                    html += `
                    <div class="trans-container align-right">
                    <div class="trans-box">
                    <div class="row">
                    <div class="col-8 trans-amount">₹ ${a.amount}</div>
                    <div class="col-4 trans-status"><span class="fa fa-check tick1" aria-hidden="true"></span>You paid</div>
                    </div>
                    <div class="row">
                    <div class="col-10 trans-id">
                    <span>Transaction ID</span>
                    <span>A12345156256787382783899</span>
                    </div>
                    <div class="col-2 trans-details"> > </div>
                    </div>
                    </div>
                    <span class="transaction-datetime">${displayDate}
                    </span>
                    </div>
                    `;
                } else if (a.type == 1 && a.direction == 2) {
                    html += `
                    <div class="trans-container align-left">
                    <div class="trans-box">
                    <div class="row">
                    <div class="col-6 trans-amount">₹ ${a.amount}</div>
                    <div class="col-6 trans-status"><span class="fa fa-paperclip attachment1" aria-hidden="true"></span>You Received</div>
                    </div>
                    <div class="row">
                    <div class="col-10 trans-id">
                    <span>Transaction ID</span>
                    <span>A12345156256787382783899</span>
                    </div>
                    <div class="col-2 trans-details"> > </div>
                    </div>
                    </div>
                    <span class="transaction-datetime">${displayDate}
                    </span>
                    </div>
                    `;
                } else if (a.type == 2 && a.direction == 1) {
                    html += `
                    <div class="trans-container align-right">
                    <div class="trans-box">
                    <div class="row">
                    <div class="col-6 trans-amount">₹ ${a.amount}</div>
                    <div class="col-6 trans-status"><span class="fa fa-check tick" aria-hidden="true"></span>You Received</div>
                    </div>
                    <div class="row">
                    <div class="col-10 requested">
                    <div class="cancel-button">Cancel</div>
                    </div>
                    <div class="col-2 trans-details"> > </div>
                    </div>
                    </div>
                    <span class="transaction-datetime">${displayDate}
                    </span>
                    </div>
                    `;
                } else if (a.type == 2 && a.direction == 2) {
                    html += `
                    <div class="trans-container align-left">
                    <div class="trans-box">
                    <div class="row">
                    <div class="col-7 trans-amount">₹ ${a.amount}</div>
                    <div class="col-5 trans-status"><span class="fa fa-paperclip attachment" aria-hidden="true"></span>                    Request Received</div>
                    </div>
                    <div class="row">
                    <div class="col-10 pay-decline">
                    <div class="pay">Pay</div>
                    <div style="flex-grow: 1"></div>
                    <div class="decline">Decline</div>
                    </div>
                    <div class="col-2 trans-details"> > </div>
                    </div>
                    </div>
                    <span class="transaction-datetime">${displayDate}
                    </span>
                    </div>
                    `;
                }

            }
        }
    }

    document.getElementById("transaction-data").innerHTML = html;

    console.log(data);

}

function getDateSet(data) {
    let arr = [];
    data.forEach((date) => {
        const temp = new Date(date.startDate);
        let res = arr.filter(item => item === temp.toLocaleDateString());
        if (res.length == 0) {
            arr.push(temp.toLocaleDateString());
        }
    });
    return arr;
}

getTransactions();








