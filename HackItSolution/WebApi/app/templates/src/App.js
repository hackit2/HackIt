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
          <Supporting txt="Sort by Score" />
      </header>
  );
}

const Supporting = (props) => {
  const sortApi = () => {
    var clicked = true;
    App.render(clicked);
  }
  return (
    <div className="extras" onClick={this.sortApi}>
      <label id="autoSort">
        <span ref="checkboxSort" className="checkbox"></span>
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

    const toSortorNotToSort = (obj,clicked) => {
      if ( clicked === true ) {
        obj.sort( (a,b) => a.nps > b.nps ).map(e => <Agent num={e.id} nps={e.nps} busy={e.busy} /> )
      } else {
        obj.map(e => <Agent num={e.id} nps={e.nps} busy={e.busy} /> )
      }
    }
  }
  
  componentDidMount() {
    
    const callThisApi = () => {
      fetch('http://http://hackit.cstairouting.com//api/state')
          .then(res => res.json())
          .then(json => {
            this.setState({
              isLoaded: true,
              items: json,

            })
          });
    }

    // const toSortorNotToSort = (obj,clicked) => {
    //   if ( clicked === true ) {
    //     obj.sort( (a,b) => a.nps > b.nps ).map(e => <Agent num={e.id} nps={e.nps} busy={e.busy} /> )
    //   } else {
    //     obj.map(e => <Agent num={e.id} nps={e.nps} busy={e.busy} /> )
    //   }
    // }

    callThisApi();

    setInterval(() => {callThisApi()}, 3000);

  }

  render(clicked) {
    var { isLoaded,items } = this.state;
    var fromJson = {};
    
    if ( !isLoaded ) {
      return <div>Loading...</div>;
    }

    else {
      fromJson['classic'] = items.classic;
      fromJson['nn'] = items.neural;

      var classic = fromJson.classic.agents;
      var nn = fromJson.nn.agents;

      return (
        <div className='container'>
            <Header title="Call Routing" subtitle="Neural Network vs. Traditional" />

            <div id="demo">

              <div id="nn">
                <h3>Neural Network Routing</h3>
                {this.toSortorNotToSort(nn)}
              </div>

              <div id="traditional">
                <h3>Traditional Routing</h3>
                {this.toSortorNotToSort(classic)}
              </div>

              <div id="statsContainer">

                <div>
                  <Stats 
                    average={nn.averageNps} 
                    total={nn.averageNps * nn.totalCalls} 
                    calls={nn.totalCalls} 
                  />
                </div>

                <div>
                  <Stats 
                    average={classic.averageNps} 
                    total={classic.averageNps * classic.totalCalls} 
                    calls={classic.totalCalls} 
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
