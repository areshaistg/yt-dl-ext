async function get_file_url() {
    const url = "http://localhost:6969/mp3?" + document.location.href;
    return await fetch(url, {
	method: "GET",
	mode: "no-cors",
    })
}

const ctrls = document.getElementsByClassName("ytp-right-controls").item(0);

function fromHTML(html, trim = true) {
  // Process the HTML string.
  html = trim ? html.trim() : html;
  if (!html) return null;

  // Then set up a new template element.
  const template = document.createElement('template');
  template.innerHTML = html;
  const result = template.content.children;

  // Then return either an HTMLElement or HTMLCollection,
  // based on whether the input HTML had one or more roots.
  if (result.length === 1) return result[0];
  return result;
}

const button = document.createElement("button")
button.classList.add("ytp-fullscreen-button")
button.classList.add("ytp-button")
button.dataset.titleNoTooltip = "Download"
button.ariaKeyShortcuts = "d"
button.ariaLabel = "Download fr"
button.title = "Download this fr"

button.appendChild(fromHTML('<svg xmlns="http://www.w3.org/2000/svg" height="100%" viewBox="0 -960 960 960" width="40px" fill="#e8eaed"><path d="M480-315.33 284.67-510.67l47.33-48L446.67-444v-356h66.66v356L628-558.67l47.33 48L480-315.33ZM226.67-160q-27 0-46.84-19.83Q160-199.67 160-226.67V-362h66.67v135.33h506.66V-362H800v135.33q0 27-19.83 46.84Q760.33-160 733.33-160H226.67Z"/></svg>'))

ctrls.appendChild(button)

button.addEventListener("click", () => {
    get_file_url()
})
