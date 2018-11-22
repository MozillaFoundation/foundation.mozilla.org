import React from 'react';
import ReactGA from '../../react-ga-proxy.js';

/**
 * A simple class for radio-group-looking things.
 */
class SelectableOption extends React.Component {
  constructor(props) {
    super(props);
  }

  forward(evt) {
    evt.preventDefault();
    evt.stopPropagation();
    this.props.onClick(this.props.label);
  }

  render() {
    return (
      <div onClick={e => this.forward(e)} className={`radio-group-entry ` + (this.props.type || `radio-button`)}>
        <span className={(this.props.square ? `square` : ``) + ` dot ` + (this.props.selected? `selected` : ``)}/> <span data-label={this.props.label} className="label">{this.props.label}</span>
      </div>
    );
  }
}

/**
 * The homepage filter system
 */
export default class Filter extends React.Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
    this.setupDocumentListeners();
  }

  getInitialState() {
    return {
      collapsed: true,
      sealOfApproval: false,
      likelihood: `Both`,
      creepinessMin: 1,
      offsetMin: `calc(0% - 14px)`,
      creepinessMax: 100,
      offsetMax: `calc(100% - 14px)`,
      trackStyle: {}
    };
  }

  setupDocumentListeners() {
    this.moveListener = evt => {
      evt.preventDefault();
      evt.stopPropagation();
      this.slideMove(evt);
    };

    this.releaseListener = evt => {
      evt.preventDefault();
      evt.stopPropagation();
      this.slideReleased(evt);
      this.removeDocumentListeners();
    };
  }

  addDocumentListeners() {
    document.addEventListener(`mousemove`, this.moveListener, true);
    document.addEventListener(`touchmove`, this.moveListener, true);
    document.addEventListener(`mouseup`, this.releaseListener, true);
    document.addEventListener(`touchstart`, this.releaseListener, true);
  }

  removeDocumentListeners() {
    document.removeEventListener(`mousemove`, this.moveListener, true);
    document.removeEventListener(`touchmove`, this.moveListener, true);
    document.removeEventListener(`mouseup`, this.releaseListener, true);
    document.removeEventListener(`touchstart`, this.releaseListener, true);
  }

  open() {
    if (this.state.collapsed) {
      let update = {
        collapsed: false
      };

      this.updateWithCSSvalues(update);
      this.setState(update);

      ReactGA.event({
        category: `buyersguide`,
        action: `filter set`,
        label: `filter on homepage`
      });
    }
  }

  close() {
    this.setState({ collapsed: true });
  }

  toggleSealOfApproval() {
    this.setState({
      sealOfApproval: !this.state.sealOfApproval
    }, () => this.setVisibilities());
  }

  handleLikelihood(label) {
    this.setState({
      likelihood: label
    }, () => this.setVisibilities());
  }

  slideStart(e) {
    this.activeSlider = e.target;

    e.preventDefault();
    e.stopPropagation();

    this.setState({
      parentBBox: this.track.getBoundingClientRect(),
      dragging: true
    });

    // The "move" and "release" events have to be handled at
    // the document level, because the events can be generated
    // "nowhere near the React-managed DOM node".
    this.addDocumentListeners();
  }

  slideReleased() {
    this.activeSlider = false;

    this.setState({
      dragging: false
    });
  }

  slideMove(e) {
    if (this.state.dragging) {
      let x = e.clientX, bbox = this.state.parentBBox;

      if (e.touches){
        x = e.touches[0].clientX;
      }

      // cap the position:
      if (x > bbox.right) {
        x = bbox.right;
      } else if (x < bbox.left) {
        x = bbox.left;
      }

      let fraction = (x-bbox.left)/bbox.width;
      let percentage = (fraction*100) | 0;
      let value = percentage ? percentage : 1;

      let update = {};
      let creepInterval = 10;

      if (this.activeSlider === this.minHead) {
        update.creepinessMin = Math.min(value, 100 - creepInterval);
        if (update.creepinessMin > this.state.creepinessMax - creepInterval) {
          update.creepinessMax = update.creepinessMin + creepInterval;
        }
      } else if(this.activeSlider === this.maxHead) {
        update.creepinessMax = Math.max(value, 1 + creepInterval);
        if (update.creepinessMax < this.state.creepinessMin + creepInterval) {
          update.creepinessMin = update.creepinessMax - creepInterval;
        }
      }

      this.updateWithCSSvalues(
        update,
        update.creepinessMin,
        update.creepinessMax
      );

      this.setState(update, () => this.setVisibilities());
    }
  }

  updateWithCSSvalues(update, min, max) {
    min = min || this.state.creepinessMin;
    max = max || this.state.creepinessMax;

    update.offsetMin = `calc(${min}% - 14px)`;
    update.offsetMax = `calc(${max}% - 14px)`;

    // Now, you'd think that given a min and max percentage,
    // the logic would be straight forward:
    //
    //   interval = max - min
    //   x-size = interval %,
    //   x-position = min %
    //
    // But that is very much not how CSS works in this case:
    // backgrounds are placed based on 0% meaning "anchor this
    // image to the left edge", but 100% meaning "anchor this
    // image to the right edge", which is rather different from
    // the usual meaning where 100% is assumed to mean "make the
    // left edge of the image coincide with the right edge of
    // the container it's a background for".
    //
    // So: we need to non-linear-maths it up, to fix that!

    let interval = (max - min),
        left = min,
        pivot = (100 - interval) / 100,
        naiveScaledLeft = left * pivot,
        difference = left - naiveScaledLeft,
        leftMatchingPercentage = left + difference/pivot;

    update.trackStyle = {
      backgroundSize: `${interval}% 100%`,
      backgroundPosition: `${leftMatchingPercentage}% center`
    };
  }

  setVisibilities() {
    let minC = this.state.creepinessMin,
        maxC = this.state.creepinessMax,
        like = this.state.likelihood,
        all = Array.from(document.querySelectorAll(`.product-box`));

    all.forEach(productBox => {
      let c = parseInt(productBox.dataset.creepiness, 10);
      let classes = productBox.classList;
      let hidden = false;

      // prefilter on seal of approval?
      if (this.state.sealOfApproval) {
        if (!productBox.querySelector(`img.seal-of-approval`)) {
          classes.add(`d-none`);
          hidden = true;
        } else {
          classes.remove(`d-none`);
        }
      }

      if (hidden) { return; }

      // Filter out for creepiness
      if (c < minC || c > maxC) {
        classes.add(`d-none`);
        hidden = true;
      } else {
        classes.remove(`d-none`);
      }

      if (hidden) { return; }

      // not hidden by creepiness: do we need to hide it due to buyers likelihood?
      let recommendation = productBox.querySelector(`.recommendation`);

      if (recommendation) {
        if (like === `Both`) {
          recommendation.classList.add(`d-none`);
          hidden = true;
        } else {
          recommendation.classList.remove(`d-none`);
        }

        if (hidden) { return; }

        if (like === `Likely` && recommendation.classList.contains(`negative`)) {
          classes.add(`d-none`);
          hidden = true;
        } else if (like === `Not likely` && recommendation.classList.contains(`positive`)) {
          classes.add(`d-none`);
          hidden = true;
        }
      }
    });
  }

  getFilterContent() {
    let mouseOpts = {
      onMouseDown: evt => this.slideStart(evt),
      onTouchStart: evt => this.slideStart(evt),
    };

    let likelihoods = [`Likely`, `Not likely`, `Both`].map(label => {
      return {
        label,
        onClick: () => this.handleLikelihood(label),
        selected: (this.state.likelihood === label)
      };
    });

    return (
      <div className={`content` + (this.state.collapsed ? ` d-none`: ``)}>
        <span className="close" onClick={() => this.close()} />

        <h2 className="filter-caption">Filter by</h2>

        <div className="seal-of-approval">
          <h3 className="h6-heading-uppercase">minimum security standards <img
            src="/_images/buyers-guide/mini-badge.svg"
            width="30px"
            height="30px"
          /></h3>
          <SelectableOption
            type="checkbox"
            label="Meets standards"
            onClick={() => this.toggleSealOfApproval()}
            selected={this.state.sealOfApproval}
            square={true}
          />
        </div>

        <div className="creepiness">
          <h3 className="h6-heading-uppercase">creepiness</h3>
          <div className="slider">
            <label>nice</label>
            <div className="track" ref={e => (this.track=e)} style={this.state.trackStyle}>
              <span className="min track-head" style={{ left: this.state.offsetMin }} ref={e => (this.minHead=e)} {...mouseOpts} />
              <span className="max track-head" style={{ left: this.state.offsetMax }} ref={e => (this.maxHead=e)} {...mouseOpts} />
            </div>
            <label className="creepy">creepy</label>
          </div>
        </div>

        <div className="likelihood">
          <h3 className="h6-heading-uppercase">likelihood to buy</h3>
          { likelihoods.map(opts => <SelectableOption {...opts}/>) }
        </div>
      </div>
    );
  }

  render() {
    let content = this.getFilterContent();

    return [
      <div className="filter-label">Filter</div>,
      <div className={`filter-content` + (this.state.collapsed ? ` collapsed` : ``)} onClick={() => this.open()}>
        { content }
      </div>
    ];
  }
}
