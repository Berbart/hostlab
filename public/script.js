document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('toggle');
  toggle.addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
  });

  fetch('/api/images')
    .then(res => res.json())
    .then(files => {
      const gallery = document.getElementById('gallery');
      files.forEach(file => {
        const img = document.createElement('img');
        img.src = `/images/${file}`;
        img.className = 'w-full h-auto';
        gallery.appendChild(img);
      });
    });
});
