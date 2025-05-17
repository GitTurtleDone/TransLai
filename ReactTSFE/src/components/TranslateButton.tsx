import type React from "react";
import { useState } from "react";
import axios from "axios";
import styles from "./FncButtons.module.css";

type languages = {
  ipt_lang_code: string;
  opt_lang_code: string;
};

const TranslateButton: React.FC<languages> = ({
  ipt_lang_code,
  opt_lang_code,
}) => {
  const [running, setRunning] = useState(false);
  const [status, setStatus] = useState("");
  const translate = async () => {
    try {
      setRunning(true);
      setStatus("Translating ... please wait");
      const response = await axios.post(
        "http://localhost:8000/translate",
        {
          ipt_lang_code: ipt_lang_code,
          opt_lang_code: opt_lang_code,
        },
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      setStatus(response.data.message || "Translated");
    } catch (err) {
      console.error(err);
      setStatus("Failed to translate");
    } finally {
      setRunning(false);
    }
  };
  return (
    <div>
      <button
        className={styles.fncButton}
        onClick={translate}
        disabled={running}
      >
        Record and Translate
      </button>
      <p>{status}</p>
    </div>
  );
};

export default TranslateButton;
