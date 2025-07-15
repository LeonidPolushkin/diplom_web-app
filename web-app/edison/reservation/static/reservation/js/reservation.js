    document.addEventListener("DOMContentLoaded", function () {
        let today = new Date().toISOString().split('T')[0];
        let dateInput = document.getElementById("reservation_date");
        let timeSelect = document.getElementById("reservation_time");

        dateInput.setAttribute("min", today);

        dateInput.addEventListener("change", function () {
            let selectedDate = this.value;
            let now = new Date();
            let currentHour = now.getHours();
            let currentMinutes = now.getMinutes();
            currentMinutes = currentMinutes < 30 ? 30 : 0;
            if (currentMinutes === 0) currentHour++;

            // Получаем занятые времена с сервера
            fetch(`/reservation/api/reserved-times/?date=${selectedDate}`)
                .then(response => response.json())
                .then(data => {
                    let reserved = data.reserved_times || [];
                    timeSelect.innerHTML = "";

                    for (let h = 14; h < 23; h++) {
                        let hour = h.toString().padStart(2, '0');
                        let t1 = `${hour}:00`;
                        let t2 = `${hour}:30`;

                        if (selectedDate === today && h < currentHour) continue;
                        if (selectedDate === today && h === currentHour && currentMinutes === 30) {
                            if (!reserved.includes(t2)) {
                                timeSelect.innerHTML += `<option value="${t2}">${t2}</option>`;
                            }
                            continue;
                        }

                        if (!reserved.includes(t1)) {
                            timeSelect.innerHTML += `<option value="${t1}">${t1}</option>`;
                        }
                        if (!reserved.includes(t2)) {
                            timeSelect.innerHTML += `<option value="${t2}">${t2}</option>`;
                        }
                    }
                });
        });
    });