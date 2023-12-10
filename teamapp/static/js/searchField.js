const fieldMenu = {
  first: [
    "be動詞",
    "be動詞過去",
    "can",
    "一般動詞",
    "一般動詞の過去",
    "過去進行形",
    "疑問詞",
    "疑問文否定文",
    "現在進行形",
    "三人称単数現在",
    "代名詞",
    "名詞の複数形",
    "命令文",
    "その他",
  ],
  second: [
    "there_is",
    "その他",
    "現在完了",
    "受け身",
    "助動詞",
    "接続詞",
    "動名詞",
    "比較",
    "不定詞",
    "不定詞2",
    "未来",
  ],
  third: ["間接疑問", "関係代名詞", "分詞", "その他"],
};
fieldMenu.all = fieldMenu.first
  .concat(fieldMenu.second)
  .concat(fieldMenu.third);

Object.keys(fieldMenu).forEach((key) => {
  console.log(key);
  fieldMenu[key] = ["ランダム"].concat(fieldMenu[key]);
});

const setMenuOptions = (selectedGrade) => {
  fieldSelect.innerHTML = "";
  fieldMenu[selectedGrade].forEach((field) => {
    const option = document.createElement("option");
    option.value = field;
    option.innerHTML = field;
    fieldSelect.appendChild(option);
  });
};

const gradeSelect = document.getElementById("grade");
const fieldSelect = document.getElementById("field");
setMenuOptions("all");

gradeSelect.addEventListener("change", (e) => {
  setMenuOptions(e.target.value);
});
