export default {
  title: "Test",
};

export const SimpleDiv = () => {
  const div = document.createElement("div");
  div.textContent = "This is a test";
  return div;
};
