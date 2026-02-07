document.addEventListener("DOMContentLoaded", () => {
  const enhance = (textarea) => {
    if (textarea.dataset.richtextBound) {
      return;
    }

    textarea.dataset.richtextBound = "true";
    textarea.style.display = "none";

    const wrapper = document.createElement("div");
    wrapper.className = "quill-wrapper";

    const toolbar = document.createElement("div");
    toolbar.className = "quill-toolbar";
    toolbar.innerHTML = `
      <span class="ql-formats">
        <select class="ql-header">
          <option value="1"></option>
          <option value="2"></option>
          <option selected></option>
        </select>
        <select class="ql-font"></select>
      </span>
      <span class="ql-formats">
        <button class="ql-bold"></button>
        <button class="ql-italic"></button>
        <button class="ql-underline"></button>
        <button class="ql-strike"></button>
      </span>
      <span class="ql-formats">
        <button class="ql-blockquote"></button>
        <button class="ql-code-block"></button>
      </span>
      <span class="ql-formats">
        <button class="ql-list" value="ordered"></button>
        <button class="ql-list" value="bullet"></button>
        <button class="ql-indent" value="-1"></button>
        <button class="ql-indent" value="+1"></button>
      </span>
      <span class="ql-formats">
        <button class="ql-link"></button>
        <button class="ql-image"></button>
      </span>
      <span class="ql-formats">
        <button class="ql-align" value=""></button>
        <button class="ql-align" value="center"></button>
        <button class="ql-align" value="right"></button>
        <button class="ql-align" value="justify"></button>
      </span>
      <span class="ql-formats">
        <button class="ql-clean"></button>
      </span>
    `;

    const editor = document.createElement("div");
    editor.className = "quill-editor";

    wrapper.appendChild(toolbar);
    wrapper.appendChild(editor);
    textarea.parentNode.insertBefore(wrapper, textarea);
    wrapper.appendChild(textarea);

    // Quill is loaded from CDN via widget Media.
    // eslint-disable-next-line no-undef
    const quill = new Quill(editor, {
      theme: "snow",
      modules: {
        toolbar: toolbar,
      },
    });

    if (textarea.value) {
      quill.clipboard.dangerouslyPasteHTML(textarea.value);
    }

    const sync = () => {
      textarea.value = quill.root.innerHTML;
    };

    quill.on("text-change", sync);
    const form = textarea.closest("form");
    if (form) {
      form.addEventListener("submit", sync);
    }
  };

  document.querySelectorAll("textarea.richtext").forEach(enhance);
});
