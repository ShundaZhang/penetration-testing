(() => {
  const search = document.getElementById('tool-search');
  const category = document.getElementById('tool-category');
  const count = document.getElementById('tool-count');
  const cards = [...document.querySelectorAll('.tool-card')];
  const zh = document.documentElement.lang.startsWith('zh');
  function filter() {
    const term = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    cards.forEach(card => {
      card.hidden = !(category.value === 'all' || category.value === card.dataset.category) || !card.textContent.toLocaleLowerCase().includes(term);
      if (!card.hidden) visible++;
    });
    count.textContent = zh ? `${visible} / ${cards.length} 项工具` : `${visible} / ${cards.length} tools`;
  }
  search.addEventListener('input', filter);
  category.addEventListener('change', filter);
  filter();
})();
