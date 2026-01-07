import html2canvas from "html2canvas";

export const exportAsImage = async (elementId) => {
  const element = document.getElementById(elementId);
  const canvas = await html2canvas(element);
  const link = document.createElement("a");
  link.download = "chart.png";
  link.href = canvas.toDataURL("image/png");
  link.click();
};
