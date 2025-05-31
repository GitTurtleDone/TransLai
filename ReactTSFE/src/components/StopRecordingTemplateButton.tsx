import type React from "react";
import { useState } from "react";
import axios from "axios";
import styles from "./FncButtons.module.css";

const StopRecordingTemplateButton: React.FC = () => {
  const [status, setStatus] = useState("");
  const [running, setRunning] = useState(false);
  const stopRecordingTemplate = async () => {
    try {
      setRunning(true);
      setStatus("Translating ...");
      const response = await axios.post(
        "http://localhost:8000/stop_recording_template",
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      console.log(response.data.message || "Template recorded.");
    } catch (err) {
      setStatus("Failed to record a template");
      console.error(err);
    } finally {
      setStatus("Recording template completed.");
      setRunning(false);
    }
  };
  return (
    <div>
      <button
        className={styles.fncButton}
        onClick={stopRecordingTemplate}
        disabled={running}
      >
        Stop
      </button>
      <p>{status}</p>
    </div>
  );
};
export default StopRecordingTemplateButton;
