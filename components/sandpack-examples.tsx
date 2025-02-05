import { Sandpack } from "@codesandbox/sandpack-react";
import { githubLight, sandpackDark } from "@codesandbox/sandpack-themes";
/**
 * The only reason this is a separate import, is so
 * we don't need to make the full page 'use client', but only this copmponent.
 */
export const SandpackExamples = () => {
  return (
    <>

<Sandpack
    files={{
      "/public/logo.svg": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-11.5 -10.23174 23 20.46348">
      <title>React Logo</title>
      <circle cx="0" cy="0" r="2.05" fill="#61dafb"/>
      <g stroke="#61dafb" stroke-width="1" fill="none">
        <ellipse rx="11" ry="4.2"/>
        <ellipse rx="11" ry="4.2" transform="rotate(60)"/>
        <ellipse rx="11" ry="4.2" transform="rotate(120)"/>
      </g>
      </svg>
      `,
            "/App.js": `

      import React, { useState, useEffect, useRef } from "react";

      export default function Game() {
        const canvasRef = useRef(null);
        const [player, setPlayer] = useState({ x: 150, y: 300, vy: -8 });
        const [platforms, setPlatforms] = useState(
          Array.from({ length: 6 }, (_, i) => ({ x: Math.random() * 300, y: i * 100 }))
        );
        const [gameOver, setGameOver] = useState(false);

        useEffect(() => {
          const handleKeyDown = (e) => {
            if (e.key === "ArrowLeft") setPlayer((p) => ({ ...p, x: p.x - 20 }));
            if (e.key === "ArrowRight") setPlayer((p) => ({ ...p, x: p.x + 20 }));
          };
          window.addEventListener("keydown", handleKeyDown);
          return () => window.removeEventListener("keydown", handleKeyDown);
        }, []);

        useEffect(() => {
          const gameLoop = setInterval(() => {
            setPlayer((p) => {
              let newY = p.y + p.vy;
              let newVy = p.vy + 0.4;
              
              if (newY > 500) {
                setGameOver(true);
              }

              let newPlatforms = platforms.map((plat) => ({ ...plat, y: plat.y + 3 }));
              newPlatforms = newPlatforms.filter((plat) => plat.y < 600);
              if (newPlatforms.length < 6) {
                newPlatforms.push({ x: Math.random() * 300, y: 0 });
              }
              setPlatforms(newPlatforms);

              for (let plat of newPlatforms) {
                if (
                  p.vy > 0 &&
                  p.y + 20 >= plat.y &&
                  p.y + 20 <= plat.y + 10 &&
                  p.x + 20 > plat.x &&
                  p.x < plat.x + 60
                ) {
                  newVy = -8;
                }
              }
              return { x: p.x, y: newY, vy: newVy };
            });
          }, 30);
          return () => clearInterval(gameLoop);
        }, [platforms]);

        return (
        <>
              <h1>Doodle Jump</h1>
            <img width="100" src="/public/logo.svg" />

          <svg width="400" height="600" className="mx-auto mt-10 border border-black bg-blue-300">
            {gameOver && (
              <rect width="400" height="600" fill="white" opacity="0.8" />
            )}
            {gameOver && (
              <text x="200" y="300" textAnchor="middle" fontSize="24" fontWeight="bold" fill="black">
                Game Over
              </text>
            )}
            {platforms.map((plat, i) => (
              <rect key={i} x={plat.x} y={plat.y} width="60" height="10" fill="green" />
            ))}
            <circle cx={player.x + 10} cy={player.y + 10} r="10" fill="red" />
          </svg>
          </>
        );
      }


      `,
    }}
    options={{
      experimental_enableServiceWorker: true,
      editorHeight: 800, // default - 300
      editorWidthPercentage: 10, // default - 50
    }}
    template="react"
  />    
      
    </>
  );
};
