const imageInput =
    document.getElementById("imageInput");


imageInput.addEventListener(
    "change",
    function () {

        const file = this.files[0];

        if (file) {

            document.getElementById(
                "fileName"
            ).textContent = file.name;

        }

    }
);


async function analyzeParking() {

    const file =
        imageInput.files[0];


    if (!file) {

        alert(
            "Please select a parking image first."
        );

        return;

    }


    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );


    document
        .getElementById("loading")
        .classList.remove("hidden");


    document
        .getElementById("dashboard")
        .classList.add("hidden");


    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/predict",
                {
                    method: "POST",
                    body: formData
                }
            );


        if (!response.ok) {

            throw new Error(
                "Prediction failed"
            );

        }


        const data =
            await response.json();


        /* STATISTICS */

        document.getElementById(
            "totalSlots"
        ).textContent =
            data.total_slots;


        document.getElementById(
            "emptySlots"
        ).textContent =
            data.empty_slots;


        document.getElementById(
            "occupiedSlots"
        ).textContent =
            data.occupied_slots;


        document.getElementById(
            "occupancyRate"
        ).textContent =
            data.occupancy_rate + "%";


        /* OCCUPANCY */

        const occupied =
            data.occupancy_rate;


        const available =
            100 - occupied;


        document.getElementById(
            "circlePercentage"
        ).textContent =
            occupied.toFixed(1) + "%";


        document.getElementById(
            "availablePercent"
        ).textContent =
            available.toFixed(1) + "%";


        document.getElementById(
            "occupiedPercent"
        ).textContent =
            occupied.toFixed(1) + "%";


        document.getElementById(
            "availableBar"
        ).style.width =
            available + "%";


        document.getElementById(
            "occupiedBar"
        ).style.width =
            occupied + "%";


        document.querySelector(
            ".occupancy-circle"
        ).style.background =
            `conic-gradient(
                #2563eb ${occupied * 3.6}deg,
                #e5e7eb ${occupied * 3.6}deg
            )`;


        /* IMAGE */

        document.getElementById(
            "resultImage"
        ).src =
            "data:image/jpeg;base64," +
            data.annotated_image;


        /* SHOW */

        document
            .getElementById("dashboard")
            .classList.remove("hidden");


        document
            .getElementById("results")
            .classList.remove("hidden");


        document
            .getElementById("slotSection")
            .classList.remove("hidden");


        /* SLOTS */

        const slotResults =
            document.getElementById(
                "slotResults"
            );


        slotResults.innerHTML = "";


        data.slots.forEach(
            slot => {

                const div =
                    document.createElement(
                        "div"
                    );


                div.classList.add(
                    "slot"
                );


                div.classList.add(
                    slot.status === "Empty"
                        ? "empty"
                        : "occupied"
                );


                div.innerHTML = `

                    <div class="slot-number">
                        SLOT ${slot.slot}
                    </div>

                    <div class="slot-status">
                        ${slot.status}
                    </div>

                    <div>
                        ${(slot.confidence * 100).toFixed(1)}%
                    </div>

                `;


                slotResults.appendChild(
                    div
                );

            }
        );


    }

    catch (error) {

        console.error(
            error
        );


        alert(
            "Could not connect to the parking server. Make sure FastAPI is running on port 8000."
        );

    }


    document
        .getElementById("loading")
        .classList.add("hidden");

}