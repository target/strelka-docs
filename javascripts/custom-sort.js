document.addEventListener('DOMContentLoaded', function () {
    // Select all tables on the page
    const tables = document.querySelectorAll('table');

    tables.forEach((table) => {
        // Select the headers in the current table
        const headers = table.querySelectorAll('th');

        headers.forEach((header, index) => {
            header.addEventListener('click', () => {
                const tbody = table.querySelector('tbody');
                const rowsArray = Array.from(tbody.querySelectorAll('tr'));
                const sortedRows = rowsArray.sort((a, b) => {
                    const aColumn = a.querySelectorAll('td')[index];
                    const bColumn = b.querySelectorAll('td')[index];
                    const aText = aColumn.textContent.trim();
                    const bText = bColumn.textContent.trim();

                    // If columns contain icons, compare their HTML to sort
                    if (aColumn.querySelector('svg') && bColumn.querySelector('svg')) {
                        return aColumn.innerHTML > bColumn.innerHTML ? 1 : -1;
                    }

                    // Otherwise, sort by text content
                    return aText.localeCompare(bText);
                });

                // Toggle sort direction
                const isAscending = header.classList.contains('ascending');
                headers.forEach(th => th.classList.remove('ascending', 'descending'));
                header.classList.add(isAscending ? 'descending' : 'ascending');

                if (isAscending) {
                    sortedRows.reverse();
                }

                // Re-add the sorted rows to the tbody
                sortedRows.forEach(row => tbody.appendChild(row));
            });
        });
    });
});
