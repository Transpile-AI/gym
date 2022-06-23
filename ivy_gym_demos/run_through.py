# global
import ivy
import argparse
import ivy_gym
from ivy_demo_utils.framework_utils import get_framework_from_str, choose_random_framework


def main(env_str=None, visualize=True, f=None):

    # Framework Setup #
    # ----------------#

    # choose random framework
    if f is None:
        f = ivy.choose_random_backend()
    else:
        if f is ivy.functional.backends.numpy:
            f = "numpy"
        elif f is ivy.functional.backends.jax:
            f = "jax"
        elif f is ivy.functional.backends.torch:
            f = "torch"
    # f = ivy.choose_random_framework() if f is None else f
    ivy.set_backend(f)

    # get environment
    env = getattr(ivy_gym, env_str)()

    # run environment steps
    env.reset()
    ac_dim = env.action_space.shape[0]
    for _ in range(250):
        ac = ivy.random_uniform(-1, 1, (ac_dim,))
        env.step(ac)
        if visualize:
            env.render()
    env.close()
    ivy.unset_backend()

    # message
    print('End of Run Through Demo!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--no_visuals', action='store_true',
                        help='whether to run the demo without rendering images.')
    parser.add_argument('--env', default='CartPole',
                        choices=['CartPole', 'Pendulum', 'MountainCar', 'Reacher', 'Swimmer'])
    parser.add_argument('--framework', type=str, default=None,
                        help='which framework to use. Chooses a random framework if unspecified.')
    parsed_args = parser.parse_args()
    framework = None if parsed_args.framework is None else get_framework_from_str(parsed_args.framework)
    main(parsed_args.env, not parsed_args.no_visuals, framework)
