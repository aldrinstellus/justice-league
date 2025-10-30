import type { Meta, StoryObj } from '@storybook/react';
import { Dashboard10 } from './Dashboard10';

const meta: Meta<typeof Dashboard10> = {
  title: 'Components/Dashboard10',
  component: Dashboard10,
  tags: ['autodocs'],
  argTypes: {
    className: {
      control: 'text',
      description: 'Additional CSS classes',
    },
  },
};

export default meta;
type Story = StoryObj<typeof Dashboard10>;

export const Default: Story = {
  args: {},
};

export const WithCustomClass: Story = {
  args: {
    className: 'bg-gray-100 p-8',
  },
};
