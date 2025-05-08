document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const source = document.getElementById("source");
    const destination = document.getElementById("destination");
    const button = form.querySelector("button");

    // Mapping airport codes to state names
    const destinationMap = {
        'IXR': 'Jharkhand',
        'DEL': 'Delhi',
        'BLK': 'Uttarakhand',
        'IXD': 'Uttar Pradesh',
        'NAG': 'Maharashtra',
        'LKO': 'Uttar Pradesh',
        'GWL': 'Madhya Pradesh'
    };

    form.addEventListener("submit", function (e) {
        if (source.value === destination.value) {
            e.preventDefault();
            alert("Source and destination cannot be the same.");
            return;
        }

        button.innerText = "Finding...";
        button.disabled = true;

        setTimeout(() => {
            button.innerText = "Find Route";
            button.disabled = false;

            // Open the landscape image search
            const destCode = destination.value;
            const state = destinationMap[destCode];
            if (state) {
                const imageSearchURL = `https://www.google.com/search?q=${state}+landscape&tbm=isch`;
                window.open(imageSearchURL, '_blank');
            }
        }, 1500); // Simulate processing delay
    });
});
