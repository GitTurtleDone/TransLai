import { useState } from "react";
import { Mic, AudioLines } from "lucide-react"; // optional: use any icon lib

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
        minWidth: "300px",
        maxWidth: "600px",
        boxSizing: "border-box",
      }}
    >
      <label>{label}</label>

      <div>
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          {languages.map((lang) => (
            <option key={lang.code} value={lang.code}>
              {lang.name}
            </option>
          ))}
        </select>
      </div>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={10}
        style={{
          minHeight: "100px",
          width: "100%",
          marginTop: "0.5rem",
          resize: "vertical", // prevent horizontal drag
        }}
      />

      <div
        style={{ display: "flex", alignItems: "center", marginTop: "0.5rem" }}
      >
        <Mic size={24} />
        <AudioLines size={24} style={{ marginLeft: "1rem" }} />
      </div>
    </div>
  );
}
