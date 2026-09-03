document.querySelector("[data-port-lookup]")?.addEventListener("submit", (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const protocol = form.get("protocol");
  const port = Number(form.get("port"));
  if ((protocol === "tcp" || protocol === "udp") && Number.isInteger(port) && port >= 0 && port <= 65535) {
    window.location.assign(`/${protocol}/${port}/`);
  }
});
