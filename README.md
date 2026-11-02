# ducu.github.io

Pagina principală: trimite la Momente, Rafturi și Sublinieri, cu câte o previzualizare.

Pagina: https://ducu.github.io/

## Ce e în repo

- `template.html`: designul paginii.
- `build.py`: scrie `index.html` din `template.html`, cu previzualizările luate din proiectele de alături (`../momente`, `../rafturi`, `../sublinieri`, ca în `~/Life`):
  - `mosaic.webp`: câte o miniatură pentru 432 de poze din Momente, alese uniform pe ani (fără story-uri);
  - `covers/`: coperțile ultimelor 7 cărți citite din Rafturi;
  - citatele scurte din Sublinieri (până la 32 de cuvinte), din care pagina alege unul la întâmplare.

GitHub Pages servește direct branch-ul `main`, fără pas de build, așa că `index.html`, `mosaic.webp` și `covers/` sunt în repo.

## Cum se actualizează

Când vrei cifrele, coperțile și pozele la zi:

```
pip3 install pillow   # o singură dată
python3 build.py
python3 -m http.server   # http://localhost:8000
git add -A && git commit -m "Actualizare" && git push
```

Atenție: `mosaic.webp` conține poze din Momente, iar repo-ul e public.
