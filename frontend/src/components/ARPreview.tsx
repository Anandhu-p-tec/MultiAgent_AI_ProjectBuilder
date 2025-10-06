import { useEffect, useRef } from "react";
import * as THREE from "three";

export default function ARPreview() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(300, 300);
    ref.current.appendChild(renderer.domElement);

    const cube = new THREE.Mesh(
      new THREE.BoxGeometry(),
      new THREE.MeshBasicMaterial({ color: 0x00ff00 })
    );
    scene.add(cube);
    camera.position.z = 2;

    function animate() {
      requestAnimationFrame(animate);
      cube.rotation.x += 0.01;
      cube.rotation.y += 0.01;
      renderer.render(scene, camera);
    }
    animate();

    return () => ref.current?.removeChild(renderer.domElement);
  }, []);

  return (
    <div>
      <h2 className="text-lg font-bold mb-4">AR Preview</h2>
      <div ref={ref}></div>
    </div>
  );
}
