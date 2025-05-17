import type React from "react";
import { useState } from "react";
import axios from "axios";
import languages from "../data/languages.json";
import styles from "./FncButtons.module.css";

const RecordTemplateButton: React.FC = () => {
  const [lang, setLang] = useState("en");
  const [status, setStatus] = useState("");
  const [running, setRunning] = useState(false);
  const record = async () => {
    try {
      setRunning(true);
      setStatus("Recording ... Wait about 3 s after that speak clearly");
      const response = await axios.post(
        "http://localhost:8000/record_template",
        {
          lang_code: lang,
        },
        { headers: { "Content-Type": "application/json" } }
      );
      setStatus(response.data.message || "Record completed");
    } catch (err) {
      console.error(err);
      setStatus("Failed to record");
    } finally {
      setRunning(false);
    }
  };
  return (
    <div>
      <button className={styles.fncButton} onClick={record} disabled={running}>
        {running ? "Recording ..." : "Start Record Template Voice"}
      </button>
      <select
        style={{ marginLeft: "2rem" }}
        value={lang}
        onChange={(e) => setLang(e.target.value)}
        disabled={running}
      >
        {languages.map((language) => (
          <option key={language.code} value={language.code}>
            {language.name}
          </option>
        ))}
        ;
      </select>
      <p> {status} </p>
    </div>
  );
};

export default RecordTemplateButton;
