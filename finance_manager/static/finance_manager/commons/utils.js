function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getYearMonth(date) {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    return `${year}-${month}`;
}

function getMonthStart(yearMonth) {
    const [year, month] = yearMonth.split('-');
    return new Date(parseInt(year), parseInt(month) - 1, 1);
}

function getMonthEnd(yearMonth) {
    const [year, month] = yearMonth.split('-');
    return new Date(parseInt(year), parseInt(month), 0);
}

function initializeMonthPicker(monthPicker) {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    monthPicker.value = `${year}-${month}`;
}
