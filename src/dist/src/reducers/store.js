/** Redux **/
import { 
  combineReducers,
  createStore,
  applyMiddleware,
} from 'redux';

/** Middleware **/
import { logger as loggerMiddleware } from 'redux-logger';
import thunkMiddleware from 'redux-thunk';

const rootReducer = combineReducers({
    /** Reducers **/
});

/** Store **/
const store = createStore(
  rootReducer,
  applyMiddleware(
    loggerMiddleware,
    thunkMiddleware,
  )
);

/** Exports **/
export default store;