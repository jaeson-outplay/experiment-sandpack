import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET(request: Request) {
    return NextResponse.json({ content: ["components/sandpack-examples.tsx","components/sandpack-examples.tsx"]});
}
