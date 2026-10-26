const express = require("express");
const { Pool } = require("pg");

const app = express();

const pool = new Pool({
    host: process.env.DB_HOST || "db",
    database: process.env.DB_NAME || "studentdb",
    user: process.env.DB_USER || "admin",
    password: process.env.DB_PASSWORD || "student123",
    port: 5432
});

app.get("/api/students", async (req, res) => {
    try {
        await pool.query(`
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        `);

        await pool.query(`
            INSERT INTO students (name)
            SELECT 'Arun'
            WHERE NOT EXISTS (
                SELECT 1 FROM students WHERE name = 'Arun'
            )
        `);

        const result = await pool.query(
            "SELECT id, name FROM students ORDER BY id"
        );

        res.json(result.rows);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get("/health", (req, res) => {
    res.json({ status: "ok" });
});

app.listen(3000, "0.0.0.0", () => {
    console.log("Backend running on port 3000");
});