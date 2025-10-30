import { render } from '@testing-library/react';
import { Settings } from './Settings';

describe('Settings', () => {
  it('renders without crashing', () => {
    render(<Settings />);
  });
});
