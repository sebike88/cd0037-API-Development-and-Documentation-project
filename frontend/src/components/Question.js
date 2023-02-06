import React, { Component } from 'react';
import '../stylesheets/Question.css';

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false,
    };
  }

  flipVisibility() {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }

  render() {
    const { questionId, question, answer, category, difficulty, rating } = this.props;
    return (
      <div className='Question-holder'>
        <div className='Question'>{question}</div>
        <div
          className="fa"
        >
          {
            Array.from(Array(5).keys()).map((index) => (
              <label
                className={`fa fa-star ${index + 1 <= rating ? 'checked' : ''}`}
                htmlFor={`rating_${questionId}_${index}`}
                data-rating={rating}
                
                key={`rating_${questionId}_${index}`}
              >
                <input id={`rating_${questionId}_${index}`} name={`rating_${questionId}`} type="radio" onClick={() =>  this.props.questionAction('PATCH', index + 1)} />
              </label>
            ))
          }
        </div>
        <div className='Question-status'>
          <img
            className='category'
            alt={`${category.toLowerCase()}`}
            src={`${category.toLowerCase()}.svg`}
          />
          <div className='difficulty'>Difficulty: {difficulty}</div>
          <img
            src='delete.png'
            alt='delete'
            className='delete'
            onClick={() => this.props.questionAction('DELETE')}
          />
        </div>
        <div
          className='show-answer button'
          onClick={() => this.flipVisibility()}
        >
          {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
        </div>
        <div className='answer-holder'>
          <span
            style={{
              visibility: this.state.visibleAnswer ? 'visible' : 'hidden',
            }}
          >
            Answer: {answer}
          </span>
        </div>
      </div>
    );
  }
}

export default Question;
