import { useEffect, useRef } from "react";
import type { QuimioinfoCard } from "../data/conteudo";

interface Props {
  card: QuimioinfoCard;
}

/** Visualização molecular didática local (Three.js), sem rede. */
export function MoleculePanel({ card }: Props) {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let disposed = false;
    let frame = 0;
    let renderer: import("three").WebGLRenderer | null = null;

    (async () => {
      const THREE = await import("three");
      if (disposed || !mountRef.current) return;
      const width = mountRef.current.clientWidth;
      const height = mountRef.current.clientHeight;
      const scene = new THREE.Scene();
      scene.background = new THREE.Color("#101820");
      const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 100);
      camera.position.set(0, 0.4, 4.2);
      renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.setSize(width, height);
      mountRef.current.innerHTML = "";
      mountRef.current.appendChild(renderer.domElement);

      const light = new THREE.DirectionalLight(0xffffff, 1.1);
      light.position.set(3, 4, 5);
      scene.add(light);
      scene.add(new THREE.AmbientLight(0x88aacc, 0.55));

      const group = new THREE.Group();
      scene.add(group);

      const isAtom = card.nome.toLowerCase().includes("carbono");
      if (isAtom) {
        const nucleus = new THREE.Mesh(
          new THREE.SphereGeometry(0.35, 32, 32),
          new THREE.MeshStandardMaterial({ color: 0xe2c98a, roughness: 0.35 }),
        );
        group.add(nucleus);
        for (let i = 0; i < 6; i++) {
          const e = new THREE.Mesh(
            new THREE.SphereGeometry(0.08, 16, 16),
            new THREE.MeshStandardMaterial({ color: 0x8fd0df }),
          );
          const angle = (i / 6) * Math.PI * 2;
          e.position.set(Math.cos(angle) * 1.2, Math.sin(angle * 2) * 0.2, Math.sin(angle) * 1.2);
          group.add(e);
        }
      } else {
        // Simplified glucose-like ring of atoms
        const colors = [0xf3efe6, 0x8fd0df, 0xe2c98a, 0xf3efe6, 0x8fd0df, 0xe2c98a];
        const atoms: import("three").Mesh[] = [];
        for (let i = 0; i < 6; i++) {
          const a = (i / 6) * Math.PI * 2;
          const mesh = new THREE.Mesh(
            new THREE.SphereGeometry(0.22, 24, 24),
            new THREE.MeshStandardMaterial({ color: colors[i], roughness: 0.4 }),
          );
          mesh.position.set(Math.cos(a) * 1.05, Math.sin(a * 2) * 0.15, Math.sin(a) * 1.05);
          group.add(mesh);
          atoms.push(mesh);
        }
        for (let i = 0; i < 6; i++) {
          const a = atoms[i].position;
          const b = atoms[(i + 1) % 6].position;
          const dir = new THREE.Vector3().subVectors(b, a);
          const len = dir.length();
          const cyl = new THREE.Mesh(
            new THREE.CylinderGeometry(0.05, 0.05, len, 10),
            new THREE.MeshStandardMaterial({ color: 0xc6a15b }),
          );
          cyl.position.copy(a).add(b).multiplyScalar(0.5);
          cyl.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.clone().normalize());
          group.add(cyl);
        }
        // hydroxyl stubs
        for (let i = 0; i < 6; i += 2) {
          const base = atoms[i].position.clone();
          const oh = new THREE.Mesh(
            new THREE.SphereGeometry(0.14, 16, 16),
            new THREE.MeshStandardMaterial({ color: 0x9e1b2e }),
          );
          oh.position.copy(base).multiplyScalar(1.45);
          group.add(oh);
        }
      }

      const onResize = () => {
        if (!mountRef.current || !renderer) return;
        const w = mountRef.current.clientWidth;
        const h = mountRef.current.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      };
      window.addEventListener("resize", onResize);

      const animate = () => {
        if (disposed || !renderer) return;
        frame = requestAnimationFrame(animate);
        group.rotation.y += 0.008;
        group.rotation.x = Math.sin(performance.now() / 1800) * 0.15;
        renderer.render(scene, camera);
      };
      animate();

      return () => {
        window.removeEventListener("resize", onResize);
      };
    })();

    return () => {
      disposed = true;
      cancelAnimationFrame(frame);
      if (renderer) {
        renderer.dispose();
        renderer.forceContextLoss();
      }
      if (mountRef.current) mountRef.current.innerHTML = "";
    };
  }, [card]);

  return <div className="molecule-stage" ref={mountRef} aria-label={`Modelo 3D de ${card.nome}`} />;
}
