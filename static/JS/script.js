$(Document).ready(function () {
    $("#load_track").submit(function () {
        $.ajax({
            type: "POST",
            url:"/",
            data: $(this).serialize(),
            success: alert("Файл успешно загружен!")
        }).done(function () {
            alert("Файл успешно загружен!")
        });
        return false;
    });
});