document.addEventListener("click", function (e) {
    if (!e.target.classList.contains("plot-fullscreen-btn")) return;

    const wrapper = e.target.closest(".plot-wrapper");

    if (!document.fullscreenElement) {
        wrapper.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
});