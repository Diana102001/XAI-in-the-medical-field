import { createChatBotMessage } from 'react-chatbot-kit';
import DynamicForm from './DynamicForm.js';
import Explanation from './Explanation.js';
import SuggestionWidget from './SuggestionWidget.js';
import useFeedbackQuestions from './MyFeedback.js';


const config = (modelid) => {
  return {
    initialMessages: [
      createChatBotMessage(`Hi! Please fill the following form`, {
        widget: "form",
        widgetProps: { modelid }, // Pass modelid to the widget
      }),
    ],
    customStyles: {
      botMessageBox: {
        backgroundColor: '#376B7E',
      },
      chatButton: {
        backgroundColor: '#5ccc9d',
      },
    },
    state: {
      suggestions: [], // You can initialize with empty suggestions
      modelid,
      
    },
    widgets: [
      {
        widgetName: 'form',
        widgetFunc: (props) => <DynamicForm {...props} modelid={modelid} />,
      },
      {
        widgetName: 'explanation',
        widgetFunc: (props) => <Explanation {...props} modelid={modelid} />,
        mapStateToProps: ["queryId"]
      },
      {
        widgetName: 'suggestionWidget',
        widgetFunc: (props) => <SuggestionWidget {...props}/>,
        mapStateToProps: ["suggestion"]
      },
      // {
      //   widgetName: 'feedback',
      //   widgetFunc: (props) => <useFeedbackQuestions {...props} />,
      //   mapStateToProps: ["queryId"]
      // },
    ],
  };
};

export default config;
