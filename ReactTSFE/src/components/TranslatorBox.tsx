import { useState } from "react";
import { Mic, AudioLines } from "lucide-react"; // optional: use any icon lib
import PlayAudio from "./PlayAudio";
type Props = {
  label: string;
  language: string;
  setLanguage: (lang: string) => void;
  text: string;
  setText: (txt: string) => void;
  languages: { code: string; name: string }[];
};

export default function TranslatorBox({
  label,
  language,
  setLanguage,
  text,
  setText,
  languages,
}: Props) {
  return (
    <div
      style={{
        flex: 1,
        minWidth: "0",
        height: "100%",
        resize: "none",
        padding: "1rem",
        fontSize: "1rem",
        // /maxWidth: "600px",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          display: "flex",
          flex: "1",
          alignItems: "baseline",
          marginTop: "0.5rem",
          width: "100%",
          gap: "1rem",
          resize: "vertical",
        }}
      >
        <label>{label}</label>
        <select
          value={language}
          onChange={(e) => {
            setLanguage(e.target.value);
            setText("");
          }}
        >
          {languages.map((lang) => (
            <option key={lang.code} value={lang.code}>
              {lang.name}
            </option>
          ))}
        </select>
        <PlayAudio
          audio_type={label == "Input" ? "ipt" : "opt"}
          lang_code={language}
        />
      </div>
      {/* <Mic size={24} />
        <AudioLines size={24} style={{ marginLeft: "1rem" }} /> */}
      {/* <div
          style={{ display: "flex", alignItems: "center", marginTop: "0.5rem" }}
        ></div> */}

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={10}
        style={{
          flex: "1",
          minHeight: "100px",
          width: "100%",
          marginTop: "0.5rem",
          resize: "vertical", // prevent horizontal drag
        }}
      />
    </div>
  );
}
