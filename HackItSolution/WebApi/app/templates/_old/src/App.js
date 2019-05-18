import React from 'react';
import './App.css';
import {jsonData} from './data.js';

const Reset = () => {
  return (
    <button onClick={console.log('reset')} id="resetBtn"><i className="fas fa-redo-alt"></i></button>
  );
}

const Agent = (props) => {
  var tag = '';

  if (props.nps <= 6) {
    tag = 'red';
  } else if (props.nps > 7) {
    tag = 'green';
  } else {
    tag = 'yellow';
  }

  return (
    <div className="agent" data-status={props.busy === true ? 'isBusy' : 'notBusy'} data-tag={tag}>
      <div>
        <span>{props.nps}</span>
        <p>{props.num}</p>
      </div>
    </div>
  );
}

const Header = (props) => {
  return (
      <header>
          <h1>{props.title}</h1>
          <h2>{props.subtitle}</h2>

          <Reset />
          <Supporting txt="Auto-Sort by Score" />
      </header>
  );
}

const Supporting = (props) => {
  return (
    <div className="extras">
      <label id="autoSort">
        <span className="checkbox"></span>
        <p>{props.txt}</p>
      </label>
    </div>
  );
}

const Stats = (props) => {
  return (
    <div className="stats">
      <span>{props.average}</span>
      <span>{props.total}</span>
      <span>{props.calls}</span>
    </div>
  );
}

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      items: [],
      isLoaded: false,
    }
  }
  
  componentDidMount() {

    fetch('http://hackit.cstairouting.com/api/state')
      .then(res => res.json())
      .then(json => {
        this.setState({
          isLoaded: true,
          items: json,

        })
      });

  }

  render() {

    // var { isLoaded,items } = this.state;
    var { items } = this.state;

    // if ( !isLoaded ) {
    //   return <div>Loading...</div>;
    // }

    // else {
      items['classic'] = jsonData.classic;
      items['nn'] = jsonData.neural

      return (
        <div className='container'>
            <Header title="Call Routing" subtitle="Neural Network vs. Traditional" />
            <div id="demo">
              <div id="nn">
                <h3>Neural Network Routing</h3>
                {items.classic.agents.map(e => 
                    <Agent 
                      num={e.id} 
                      nps={e.nps} 
                      busy={e.busy} 
                    />    
                )}
              </div>

              <div id="traditional">
              <h3>Traditional Routing</h3>
                {items.nn.agents.map(e => 
                    <Agent num={e.id} nps={e.nps} />    
                )}

              </div>

              <div id="statsContainer">
                <div>
                <Stats 
                  average={items.classic.averageNps} 
                  total={items.classic.averageNps * items.classic.totalCalls} 
                  calls={items.classic.totalCalls} 
                />
                </div>
                <div>
                <Stats 
                  average={items.classic.averageNps} 
                  total={items.classic.averageNps * items.classic.totalCalls} 
                  calls={items.classic.totalCalls} 
                />
                </div>
              </div>
            </div>
        </div>
      );

    //}

  }

}

export default App;
