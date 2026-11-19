#!/usr/bin/env python3
"""
guebly-downloader — wrapper yt-dlp para análise competitiva de canais
Uso: python guebly-downloader.py <url-ou-@handle> [opcoes]

Exemplos:
  python guebly-downloader.py @chicotedafofoca --thumbs --top 10
  python guebly-downloader.py @anaodoreddit --video --top 5
  python guebly-downloader.py @natanporai --info --top 20
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_OUT = Path("./downloads")

SHORTS_SUFFIX = "/shorts"


def run(cmd: list[str], capture=True):
    result = subprocess.run(cmd, capture_output=capture, text=True)
    if result.returncode != 0 and capture:
        print(f"[erro] {result.stderr[-300:]}", file=sys.stderr)
    return result


def resolve_url(handle_or_url: str) -> str:
    if handle_or_url.startswith("http"):
        return handle_or_url
    h = handle_or_url.lstrip("@")
    return f"https://www.youtube.com/@{h}{SHORTS_SUFFIX}"


def download_thumbs(url: str, out: Path, top: int):
    """Baixa thumbnails + JSON metadata sem baixar vídeo."""
    out.mkdir(parents=True, exist_ok=True)
    cmd = [
        "yt-dlp",
        "--write-thumbnail",
        "--write-info-json",
        "--skip-download",
        "--playlist-items", f"1-{top}",
        "-o", str(out / "%(channel)s/%(id)s.%(ext)s"),
        url,
    ]
    print(f"[thumbs] baixando top {top} de {url}")
    run(cmd, capture=False)


def download_videos(url: str, out: Path, top: int, quality: str = "720"):
    """Baixa vídeos + thumbnail + metadata."""
    out.mkdir(parents=True, exist_ok=True)
    cmd = [
        "yt-dlp",
        "--write-thumbnail",
        "--write-info-json",
        "--playlist-items", f"1-{top}",
        "--format", f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]",
        "-o", str(out / "%(channel)s/%(id)s.%(ext)s"),
        url,
    ]
    print(f"[video] baixando top {top} de {url} ({quality}p)")
    run(cmd, capture=False)


def download_info(url: str, out: Path, top: int):
    """Baixa apenas JSON metadata (views, título, duração, likes)."""
    out.mkdir(parents=True, exist_ok=True)
    cmd = [
        "yt-dlp",
        "--write-info-json",
        "--skip-download",
        "--no-write-thumbnail",
        "--playlist-items", f"1-{top}",
        "-o", str(out / "%(channel)s/%(id)s.%(ext)s"),
        url,
    ]
    print(f"[info] baixando metadata top {top} de {url}")
    run(cmd, capture=False)


def print_summary(out: Path):
    """Lê todos os .info.json baixados e imprime resumo de views."""
    jsons = list(out.rglob("*.info.json"))
    if not jsons:
        print("[summary] nenhum .info.json encontrado")
        return

    videos = []
    for f in jsons:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            videos.append({
                "titulo": data.get("title", "?")[:60],
                "views": data.get("view_count", 0),
                "duracao": data.get("duration_string", "?"),
                "id": data.get("id", "?"),
                "canal": data.get("channel", "?"),
            })
        except Exception:
            pass

    videos.sort(key=lambda v: v["views"] or 0, reverse=True)
    print(f"\n{'VIEWS':>10}  {'DUR':>6}  TITULO")
    print("-" * 70)
    for v in videos[:20]:
        views = f"{v['views']:,}" if v["views"] else "?"
        print(f"{views:>10}  {v['duracao']:>6}  {v['titulo']}")


def main():
    p = argparse.ArgumentParser(description="guebly-downloader — análise competitiva")
    p.add_argument("url", help="URL ou @handle do canal/vídeo")
    p.add_argument("--thumbs", action="store_true", help="Baixar thumbnails + metadata")
    p.add_argument("--video", action="store_true", help="Baixar vídeos")
    p.add_argument("--info", action="store_true", help="Baixar apenas metadata JSON")
    p.add_argument("--top", type=int, default=10, help="Quantos vídeos (padrão: 10)")
    p.add_argument("--quality", default="720", help="Qualidade máxima em px (padrão: 720)")
    p.add_argument("--out", default=str(DEFAULT_OUT), help="Pasta de saída")
    p.add_argument("--summary", action="store_true", help="Imprimir resumo de views dos JSONs já baixados")
    args = p.parse_args()

    out = Path(args.out)
    url = resolve_url(args.url)

    if args.summary:
        print_summary(out)
        return

    if not any([args.thumbs, args.video, args.info]):
        args.thumbs = True  # default: só thumbnails

    if args.thumbs:
        download_thumbs(url, out, args.top)
    if args.video:
        download_videos(url, out, args.top, args.quality)
    if args.info:
        download_info(url, out, args.top)

    print_summary(out)


if __name__ == "__main__":
    main()
