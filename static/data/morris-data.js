$(function() {

    Morris.Bar({
        element: 'morris-bar-chart',
        data: [
          {y:'AndreaD.',a:322,b:341},
          {y:'Ellie',a:185,b:193},
          {y:'Rexx',a:128,b:133},
          {y:'Heather',a:110,b:111},
          {y:'Cayla',a:107,b:107}
        ],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['Total Paid Visits', 'Total Visits'],
        hideHover: 'auto',
        resize: true
    });

    Morris.Donut({
        element: 'morris-donut-chart',
        data: [{
            label: "Paid Visits",
            value: 2070
        }, {
            label: "Guest Visits",
            value: 52
        }],
        resize: true
    });

});
