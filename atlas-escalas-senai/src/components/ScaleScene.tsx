import { useEffect, useRef } from "react";
import type { ScaleId } from "../data/conteudo";
import { CELL_HUD } from "../data/conteudo";

interface Props {
  scaleId: ScaleId;
}

function drawRoundedRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  r: number,
) {
  const radius = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.arcTo(x + w, y, x + w, y + h, radius);
  ctx.arcTo(x + w, y + h, x, y + h, radius);
  ctx.arcTo(x, y + h, x, y, radius);
  ctx.arcTo(x, y, x + w, y, radius);
  ctx.closePath();
}

export function ScaleScene({ scaleId }: Props) {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let raf = 0;
    let t0 = performance.now();

    const resize = () => {
      const parent = canvas.parentElement;
      if (!parent) return;
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const { width, height } = parent.getBoundingClientRect();
      canvas.width = Math.max(1, Math.floor(width * dpr));
      canvas.height = Math.max(1, Math.floor(height * dpr));
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    resize();
    window.addEventListener("resize", resize);

    const paint = (now: number) => {
      const parent = canvas.parentElement;
      if (!parent) return;
      const { width: w, height: h } = parent.getBoundingClientRect();
      const t = (now - t0) / 1000;
      ctx.clearRect(0, 0, w, h);

      // shared vignette field
      const g = ctx.createRadialGradient(w * 0.5, h * 0.48, 20, w * 0.5, h * 0.5, Math.max(w, h) * 0.7);
      g.addColorStop(0, "rgba(158,27,46,0.18)");
      g.addColorStop(0.45, "rgba(31,78,95,0.12)");
      g.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, w, h);

      if (scaleId === "organismo") {
        ctx.save();
        ctx.translate(w * 0.55, h * 0.52);
        ctx.strokeStyle = "rgba(243,239,230,0.75)";
        ctx.lineWidth = 2.2;
        ctx.beginPath();
        ctx.ellipse(0, -110, 34, 42, 0, 0, Math.PI * 2);
        ctx.moveTo(0, -68);
        ctx.lineTo(0, 40);
        ctx.moveTo(0, -40);
        ctx.lineTo(-55, 10);
        ctx.moveTo(0, -40);
        ctx.lineTo(55, 10);
        ctx.moveTo(0, 40);
        ctx.lineTo(-35, 120);
        ctx.moveTo(0, 40);
        ctx.lineTo(35, 120);
        ctx.stroke();
        ctx.restore();
      }

      if (scaleId === "orgao") {
        ctx.save();
        ctx.translate(w * 0.58, h * 0.5);
        const beat = 1 + Math.sin(t * 3.2) * 0.04;
        ctx.scale(beat, beat);
        ctx.fillStyle = "rgba(158,27,46,0.88)";
        ctx.beginPath();
        ctx.moveTo(0, 28);
        ctx.bezierCurveTo(-70, -10, -55, -70, 0, -40);
        ctx.bezierCurveTo(55, -70, 70, -10, 0, 28);
        ctx.fill();
        ctx.restore();
      }

      if (scaleId === "tecido") {
        for (let i = 0; i < 9; i++) {
          const y = h * 0.25 + i * 28;
          ctx.strokeStyle = `rgba(226,201,138,${0.25 + (i % 3) * 0.12})`;
          ctx.lineWidth = 6;
          ctx.beginPath();
          ctx.moveTo(w * 0.28, y);
          ctx.bezierCurveTo(w * 0.45, y - 12, w * 0.55, y + 12, w * 0.78, y);
          ctx.stroke();
        }
      }

      if (scaleId === "celula") {
        const cx = w * 0.58;
        const cy = h * 0.48;
        // crimson cell body with top cut (sectioned edge)
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(cx - 150, cy - 40);
        ctx.quadraticCurveTo(cx - 170, cy + 120, cx, cy + 145);
        ctx.quadraticCurveTo(cx + 170, cy + 120, cx + 150, cy - 40);
        ctx.lineTo(cx + 90, cy - 95);
        ctx.quadraticCurveTo(cx, cy - 70, cx - 90, cy - 95);
        ctx.closePath();
        const cellGrad = ctx.createLinearGradient(cx, cy - 120, cx, cy + 150);
        cellGrad.addColorStop(0, "#7a1424");
        cellGrad.addColorStop(0.45, "#b02036");
        cellGrad.addColorStop(1, "#4a0d18");
        ctx.fillStyle = cellGrad;
        ctx.fill();

        // grey accumulated stain patches
        ctx.globalAlpha = 0.35;
        ctx.fillStyle = "#8d9094";
        for (const [ox, oy, rw, rh] of [
          [-40, 10, 70, 36],
          [45, 55, 55, 28],
          [-70, 70, 40, 24],
        ] as const) {
          drawRoundedRect(ctx, cx + ox, cy + oy, rw, rh, 12);
          ctx.fill();
        }
        ctx.globalAlpha = 1;

        // gold network
        ctx.strokeStyle = "rgba(226,201,138,0.75)";
        ctx.lineWidth = 1.4;
        for (let i = 0; i < 18; i++) {
          const a = (i / 18) * Math.PI * 2 + t * 0.15;
          ctx.beginPath();
          ctx.moveTo(cx, cy + 10);
          ctx.quadraticCurveTo(
            cx + Math.cos(a) * 70,
            cy + Math.sin(a) * 55,
            cx + Math.cos(a) * 120,
            cy + 20 + Math.sin(a) * 90,
          );
          ctx.stroke();
        }

        // amber mitochondria at corners
        const corners = [
          [cx - 95, cy + 35],
          [cx + 100, cy + 20],
          [cx + 20, cy + 105],
        ] as const;
        for (const [mx, my] of corners) {
          ctx.fillStyle = "rgba(184,107,42,0.9)";
          ctx.beginPath();
          ctx.ellipse(mx, my, 22, 12, 0.5, 0, Math.PI * 2);
          ctx.fill();
          ctx.strokeStyle = "rgba(255,220,160,0.55)";
          ctx.beginPath();
          ctx.moveTo(mx - 12, my);
          ctx.quadraticCurveTo(mx, my - 6, mx + 12, my);
          ctx.stroke();
        }

        // nuclear mesh
        ctx.strokeStyle = "rgba(226,201,138,0.65)";
        ctx.beginPath();
        ctx.arc(cx - 10, cy + 5, 28, 0, Math.PI * 2);
        ctx.stroke();
        for (let i = 0; i < 6; i++) {
          const a = (i / 6) * Math.PI * 2;
          ctx.beginPath();
          ctx.arc(cx - 10 + Math.cos(a) * 10, cy + 5 + Math.sin(a) * 10, 4, 0, Math.PI * 2);
          ctx.stroke();
        }

        // ER ring
        ctx.strokeStyle = "rgba(243,239,230,0.35)";
        ctx.setLineDash([4, 5]);
        ctx.beginPath();
        ctx.ellipse(cx + 35, cy - 5, 48, 28, -0.4, 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);

        // glass vesicles
        for (const [vx, vy, r] of [
          [cx + 70, cy - 35, 8],
          [cx - 55, cy - 20, 6],
          [cx + 5, cy + 70, 7],
        ] as const) {
          ctx.fillStyle = "rgba(220,230,235,0.22)";
          ctx.strokeStyle = "rgba(255,255,255,0.35)";
          ctx.beginPath();
          ctx.arc(vx, vy + Math.sin(t + vx) * 2, r, 0, Math.PI * 2);
          ctx.fill();
          ctx.stroke();
        }

        // gold edge connectors
        ctx.fillStyle = "#e2c98a";
        for (const [px, py] of [
          [cx - 90, cy - 95],
          [cx + 90, cy - 95],
          [cx - 150, cy - 40],
          [cx + 150, cy - 40],
        ] as const) {
          ctx.beginPath();
          ctx.arc(px, py, 3.5, 0, Math.PI * 2);
          ctx.fill();
        }

        // floating fragment particles
        ctx.fillStyle = "rgba(180,185,190,0.55)";
        for (let i = 0; i < 12; i++) {
          const fx = cx - 140 + ((i * 37 + t * 18) % 280);
          const fy = cy - 110 + Math.sin(t + i) * 8 + (i % 5) * 12;
          ctx.fillRect(fx, fy, 3, 3);
        }
      }

      if (scaleId === "organela") {
        const cx = w * 0.58;
        const cy = h * 0.5;
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(0.35 + Math.sin(t * 0.5) * 0.03);
        ctx.fillStyle = "#b86b2a";
        ctx.beginPath();
        ctx.ellipse(0, 0, 130, 70, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "rgba(255,220,170,0.55)";
        ctx.lineWidth = 2;
        for (let i = -3; i <= 3; i++) {
          ctx.beginPath();
          ctx.moveTo(-100, i * 12);
          ctx.bezierCurveTo(-30, i * 12 - 18, 30, i * 12 + 18, 100, i * 12);
          ctx.stroke();
        }
        ctx.restore();
      }

      if (scaleId === "molecula") {
        const cx = w * 0.58;
        const cy = h * 0.5;
        const nodes = [
          [0, 0],
          [40, -28],
          [78, 0],
          [40, 34],
          [-38, -30],
          [-70, 8],
          [-30, 40],
        ];
        ctx.strokeStyle = "rgba(226,201,138,0.8)";
        ctx.lineWidth = 3;
        ctx.beginPath();
        for (let i = 0; i < nodes.length; i++) {
          const [x, y] = nodes[i];
          if (i === 0) ctx.moveTo(cx + x, cy + y);
          else ctx.lineTo(cx + x, cy + y);
        }
        ctx.closePath();
        ctx.stroke();
        for (const [x, y] of nodes) {
          ctx.fillStyle = iColor(x);
          ctx.beginPath();
          ctx.arc(cx + x, cy + y + Math.sin(t + x) * 2, 10, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      if (scaleId === "atomo") {
        const cx = w * 0.58;
        const cy = h * 0.5;
        ctx.fillStyle = "#e2c98a";
        ctx.beginPath();
        ctx.arc(cx, cy, 16, 0, Math.PI * 2);
        ctx.fill();
        for (let i = 0; i < 3; i++) {
          ctx.strokeStyle = `rgba(243,239,230,${0.35 + i * 0.15})`;
          ctx.beginPath();
          ctx.ellipse(cx, cy, 50 + i * 28, 22 + i * 8, (i * Math.PI) / 3 + t * 0.4, 0, Math.PI * 2);
          ctx.stroke();
          const a = t * (1.2 + i * 0.3) + i;
          const rx = 50 + i * 28;
          const ry = 22 + i * 8;
          const rot = (i * Math.PI) / 3 + t * 0.4;
          const ex = cx + Math.cos(a) * rx * Math.cos(rot) - Math.sin(a) * ry * Math.sin(rot);
          const ey = cy + Math.cos(a) * rx * Math.sin(rot) + Math.sin(a) * ry * Math.cos(rot);
          ctx.fillStyle = "#9ec9d8";
          ctx.beginPath();
          ctx.arc(ex, ey, 5, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      raf = requestAnimationFrame(paint);
    };

    raf = requestAnimationFrame(paint);
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
    };
  }, [scaleId]);

  return (
    <>
      <canvas ref={ref} className="scene-canvas" aria-label={`Cena da escala ${scaleId}`} />
      {scaleId === "celula" && (
        <div className="hud-strip pulse" aria-live="polite">
          <div className="hud-title">{CELL_HUD.titulo}</div>
          <div style={{ fontSize: "0.85rem", opacity: 0.9 }}>{CELL_HUD.subtitulo}</div>
          <div className="hud-metrics">
            {CELL_HUD.metricas.map((m) => (
              <div key={m.rotulo}>
                <div style={{ opacity: 0.7 }}>{m.rotulo}</div>
                <strong>{m.valor}</strong>
              </div>
            ))}
          </div>
          <div style={{ fontSize: "0.78rem", color: "#e2c98a" }}>
            Ciclo de colorações: {CELL_HUD.ciclo}
          </div>
        </div>
      )}
    </>
  );
}

function iColor(x: number) {
  if (x > 50) return "#8fd0df";
  if (x < -20) return "#e2c98a";
  return "#f3efe6";
}
