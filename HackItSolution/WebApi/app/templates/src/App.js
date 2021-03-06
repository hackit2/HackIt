import React from 'react';
import './App.css';

// import {jsonData} from './data.js';

// const apiInvoker = (obj) => {
//   obj.setState.items = callApi();
// }

// const callApi = async () => {
//   const response = await fetch('http://localhost:5000/api/state');
//   const json = await response.json();

//   return json;
// }

class Reset extends React.Component {
  constructor(props) {
    super(props)
  }

  resetFn() {
    fetch(`${window.location.protocol}//${window.location.host.replace("localhost:3000","localhost:5000")}/api/state/reset`, {
      method: 'POST'
    });
  }
  
  render() {
    return (
      <button id="resetBtn" onClick={this.resetFn}><i className="fas fa-redo-alt"></i></button>
    );
  }
}

const Agent = (props) => {
  var tag = '';

  if (props.nps <= 5) {
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
          <Improvement per={props.percImproved} />
          {/* <Supporting txt="Sort by Score" /> */}
      </header>
  );
}

const Improvement = (props) => {
    return (
      <h4>Neural Network Percent Improvement: <span>{props.per}%</span></h4>
    );
}

// class Supporting extends React.Component {
//   constructor(props) {
//     super(props)

//     this.sortApi = () => {
//       var clicked = true;
//       App.render(clicked);
//     }
//   }
  
//   render(){
//     return (
//       <div className="extras" onClick={this.sortApi()}>
//         <label id="autoSort">
//           <span ref="checkboxSort" className="checkbox"></span>
//           <p>{this.props.txt}</p>
//         </label>
//       </div>
//     );
//   }
// }

const Stats = (props) => {
  return (
    <div className="stats">
      <span>{props.average}<p>Avg. NPS</p></span>
      <span>{props.total}<p>Total NPS</p></span>
      <span>{props.calls}<p>Total Calls</p></span>
    </div>
  );
}

const Header3 = (props) => {
  return (
    <h3>{props.txt}</h3>
  );
}

const ToSort = (props) => {
  var sorted = props.obj;

  if (props.status === true) {
    sorted = props.obj.sort( (a,b) => a.nps > b.nps )
  }

  return (
    <div id={props.id}>
      <Header3 txt={props.txt} />
      {sorted.map(e => <Agent num={e.id} nps={e.nps} busy={e.busy} /> )}
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

    let host = `${window.location.protocol}//${window.location.host.replace("localhost:3000","localhost:5000")}`
    const callThisApi = () => {
      
      fetch(host+'/api/state')
          .then(res => res.json())
          .then(json => {
            if (json !== null) {
              this.setState({
                isLoaded: true,
                items: json,

              })
            }
          });
    }

    callThisApi();
    setInterval(() => {callThisApi()}, 3000);

  }

  render(clicked) {
    var { isLoaded,items } = this.state;
    var fromJson = {};
    
    if ( !isLoaded ) {
      return (
        <div className='container'>
            <Header title=".Predict()" subtitle="Neural Network vs. Traditional Call Routing" />

            <div id="demo">
              <div>Loading...</div>;
            </div>
        </div>
      )
    }

    else {
      fromJson['classic'] = items.classic;
      fromJson['nn'] = items.neural;

      var classic = fromJson.classic.agents;
      var nn = fromJson.nn.agents;

      return (
        <div className='container'>
            <Header title=".Predict()" subtitle="Neural Network vs. Traditional Call Routing" percImproved={fromJson.nn.percentImprovement} />

            <div id="demo">

              <ToSort obj={nn} status={clicked} txt="Neural Network Routing" id="nn" />
              <ToSort obj={classic} status={clicked} txt="Traditional Routing" id="traditional" />              

              <div id="statsContainer">
                <div>
                  <Stats 
                    average={fromJson.nn.averageNps} 
                    total={fromJson.nn.totalNps} 
                    calls={fromJson.nn.totalCalls} 
                  />
                </div>
                <div>
                  <Stats 
                    average={fromJson.classic.averageNps} 
                    total={fromJson.classic.totalNps} 
                    calls={fromJson.classic.totalCalls} 
                  />
                </div>
              </div>
            </div>
        </div>
      );

    }

  }

}

export default App;
