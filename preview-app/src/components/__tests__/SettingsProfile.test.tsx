import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import SettingsProfile from '../SettingsProfile';

describe('SettingsProfile', () => {
  it('renders the settings page header', () => {
    render(<SettingsProfile />);
    expect(screen.getByRole('heading', { name: /settings/i })).toBeInTheDocument();
  });

  it('renders sidebar navigation with all menu items', () => {
    render(<SettingsProfile />);
    expect(screen.getByText('Profile')).toBeInTheDocument();
    expect(screen.getByText('Account')).toBeInTheDocument();
    expect(screen.getByText('Members')).toBeInTheDocument();
    expect(screen.getByText('Billing')).toBeInTheDocument();
    expect(screen.getByText('Invoices')).toBeInTheDocument();
    expect(screen.getByText('API')).toBeInTheDocument();
  });

  it('renders basic information form', () => {
    render(<SettingsProfile />);
    expect(screen.getByRole('heading', { name: /basic information/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/first name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/last name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
  });

  it('renders change password form', () => {
    render(<SettingsProfile />);
    expect(screen.getByRole('heading', { name: /change password/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/verify current password/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/new password/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument();
  });

  it('renders advanced settings with checkboxes', () => {
    render(<SettingsProfile />);
    expect(screen.getByRole('heading', { name: /advanced settings/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/data export access/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/allow admin to add members/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/enable two-factor authentication/i)).toBeInTheDocument();
  });

  it('has all checkboxes checked by default', () => {
    render(<SettingsProfile />);
    const dataExport = screen.getByLabelText(/data export access/i);
    const adminMembers = screen.getByLabelText(/allow admin to add members/i);
    const twoFactor = screen.getByLabelText(/enable two-factor authentication/i);

    expect(dataExport).toBeChecked();
    expect(adminMembers).toBeChecked();
    expect(twoFactor).toBeChecked();
  });

  it('allows toggling checkboxes', async () => {
    const user = userEvent.setup();
    render(<SettingsProfile />);

    const dataExport = screen.getByLabelText(/data export access/i);
    expect(dataExport).toBeChecked();

    await user.click(dataExport);
    expect(dataExport).not.toBeChecked();

    await user.click(dataExport);
    expect(dataExport).toBeChecked();
  });

  it('renders all save buttons', () => {
    render(<SettingsProfile />);
    const saveButtons = screen.getAllByRole('button', { name: /save/i });
    expect(saveButtons).toHaveLength(3); // One for each section
  });

  it('has accessible form inputs', () => {
    render(<SettingsProfile />);
    const usernameInput = screen.getByLabelText(/username/i);
    expect(usernameInput).toHaveAttribute('type', 'text');
    expect(usernameInput).toHaveValue('nicol43');
  });

  it('password fields have correct type', () => {
    render(<SettingsProfile />);
    const currentPassword = screen.getByLabelText(/verify current password/i);
    const newPassword = screen.getByLabelText(/new password/i);
    const confirmPassword = screen.getByLabelText(/confirm password/i);

    expect(currentPassword).toHaveAttribute('type', 'password');
    expect(newPassword).toHaveAttribute('type', 'password');
    expect(confirmPassword).toHaveAttribute('type', 'password');
  });

  it('search input is present in header', () => {
    render(<SettingsProfile />);
    const searchInput = screen.getByPlaceholderText(/search/i);
    expect(searchInput).toBeInTheDocument();
    expect(searchInput).toHaveAttribute('type', 'search');
  });

  it('renders upgrade button', () => {
    render(<SettingsProfile />);
    expect(screen.getByRole('button', { name: /upgrade/i })).toBeInTheDocument();
  });
});
