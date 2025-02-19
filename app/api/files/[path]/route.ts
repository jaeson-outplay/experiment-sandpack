import { NextResponse } from "next/server";
import { promises as fs } from "fs";
import path from "path";

export async function GET(req: Request) {
    const { searchParams } = new URL(req.url);
    const filePath = searchParams.get("path");

    if (!filePath) {
        return NextResponse.json({ error: "File path is required" }, { status: 400 });
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