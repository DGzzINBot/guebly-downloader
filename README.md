# guebly-downloader

Wrapper [yt-dlp](https://github.com/yt-dlp/yt-dlp) para análise competitiva de canais YouTube/TikTok.
Usado pela equipe Guebly/Trendly para baixar thumbnails, metadata e vídeos virais de canais concorrentes.

## Instalação

```bash
pip install yt-dlp
# ffmpeg também necessário para extração de frames
```

## Uso

```bash
# Baixar thumbnails + metadata dos top 10 vídeos de um canal
python guebly_downloader.py @chicotedafofoca --thumbs --top 10

# Baixar vídeos virais top 5 (qualidade 480p)
python guebly_downloader.py @natanporai --video --top 5 --quality 480

# Só metadata/views (mais rápido)
python guebly_downloader.py @pipocaefofoca --info --top 20

# Resumo de views dos que já baixou
python guebly_downloader.py . --summary --out ./downloads

# Usando URL direta
python guebly_downloader.py "https://www.youtube.com/@anaodoreddit/shorts" --thumbs --top 15
```

## Nichos analisados pela Trendly

| Canal | Nicho | Subs |
|---|---|---|
| @natanporai | Fofoca/Entretenimento | 57.3M |
| @mepoupe | Finanças | 7.6M |
| @opricorico | Finanças | 7M |
| @nandopinheiro | Motivação | 2M |
| @betoribeirocrime | True Crime | 2.4M |
| @anaodoreddit | Confissão/Reddit | 67K |
| @pipocaefofoca | Fofoca | 507K |
| @chicotedafofoca | Fofoca | — |

## Saída

Cada download cria:
- `downloads/<canal>/<video_id>.jpg` — thumbnail
- `downloads/<canal>/<video_id>.info.json` — metadata completa (views, likes, título, duração)

## Resumo de views

```bash
python guebly_downloader.py . --summary
# VIEWS      DUR  TITULO
# 3,400,000  0:28  Que choque! Famoso revela...
# 2,100,000  0:15  Ninguém esperava isso...
```
