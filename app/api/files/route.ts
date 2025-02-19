import { NextRequest, NextResponse } from 'next/server';
import { promises as fs } from "fs";
import path from "path";

export async function GET(request: Request) {
    const { searchParams } = new URL(request.url);
    const filePath = searchParams.get("path");

    if (!filePath) {
        return NextResponse.json({ content: ["components/sandpack-examples.tsx","components/sandpack-styles.tsx"]});
    }

    try {
        // Ensure the file path is inside the project directory for security check
        const projectRoot = process.cwd();
        const resolvedPath = path.resolve(projectRoot, filePath);

        if (!resolvedPath.startsWith(projectRoot)) {
        return NextResponse.json({ error: "Access denied" }, { status: 403 });
        }

        // Read file content
        const fileContent = await fs.readFile(resolvedPath, "utf-8");

        return NextResponse.json({ content: fileContent, path: resolvedPath });
    } catch (error) {
        return NextResponse.json({ error: "File not found or unreadable" }, { status: 404 });
    }
}

export async function PUT(req: Request) {
    if (req.body){
        try {
            const { searchParams } = new URL(req.url);
            const filePath = searchParams.get("path");
            const buffer = await req.arrayBuffer();
            const decoder = new TextDecoder("utf-8");
            const content = decoder.decode(buffer);
            if (!filePath || !content) {
            return NextResponse.json({ error: "File path and content are required" }, { status: 400 });
            }
    
            const projectRoot = process.cwd();
            const resolvedPath = path.resolve(projectRoot, filePath);
    
            // Security check to prevent modifying files outside the project
            if (!resolvedPath.startsWith(projectRoot)) {
            return NextResponse.json({ error: "Access denied" }, { status: 403 });
            }
            await fs.writeFile(resolvedPath, content, "utf-8");
            return NextResponse.json({ message: "File updated successfully", path: "resolvedPath" });
        } catch (error) {
            return NextResponse.json({ error: "Failed to update file" }, { status: 500 });
        }
    } else {
        return NextResponse.json({ error: "No body" }, { status: 400 });
    }
}
