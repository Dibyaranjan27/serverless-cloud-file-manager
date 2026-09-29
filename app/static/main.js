document.getElementById('fileInput').addEventListener('change', function(e) {
    var files = e.target.files;
    var display = document.getElementById('fileName');
    if (files.length === 0) {
        display.textContent = 'No files selected';
    } else if (files.length === 1) {
        display.textContent = files[0].name;
    } else {
        display.textContent = files.length + ' files selected';
    }
});

var searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('keyup', function() {
        var filter = this.value.toLowerCase();
        var rows = document.querySelectorAll('tbody tr');
        
        rows.forEach(function(row) {
            var filename = row.cells[0].textContent.toLowerCase();
            if (filename.includes(filter)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
}
