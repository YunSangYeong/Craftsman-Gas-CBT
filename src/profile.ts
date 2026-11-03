// Q-Net could not be accessed during preparation. These are explicitly
// provisional learning settings, not a claim of verified official rules.
export const PROFILE = {
  name: "가스기능사",
  subjects: ["가스일반", "가스장치 및 기기", "가스안전관리"] as const,
  questionCount: 60,
  durationMinutes: 60,
  choiceCount: 4,
  passScore: 60,
  subjectCutoff: false,
  learningQuestionsPerSubject: 20,
  rulesVerificationStatus: "pending",
  officialSource: "https://www.q-net.or.kr/crf005.do?id=crf00503&jmCd=6335",
  selectionPolicy: "학습용 세 영역 각 20문항. 공식 과목별 출제 비율이 아님",
};
